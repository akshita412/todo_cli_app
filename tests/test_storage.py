# agent-notes: ctx="storage backend tests — M2 JSON and SQLite" deps=["todo_cli.storage.json_store","todo_cli.models"] state=active last="tara@2026-06-23"

import json
import os
from pathlib import Path

import pytest
from todo_cli.exceptions import StorageAccessError, StorageCorruptError
from todo_cli.models import Task, Status
from todo_cli.storage.json_store import JsonStorageBackend


@pytest.fixture
def store(tmp_path):
    return JsonStorageBackend(data_dir=tmp_path)


def test_add_returns_task_with_assigned_id(store):
    task = Task(description="Buy milk", status=Status.PENDING)
    result = store.add(task)
    assert result.id == 1


def test_get_returns_task_by_id(store):
    task = Task(description="Buy milk", status=Status.PENDING)
    store.add(task)
    result = store.get(1)
    assert result is not None
    assert result.description == "Buy milk"


def test_get_returns_none_for_missing_id(store):
    assert store.get(999) is None


def test_list_returns_all_tasks_sorted_by_created_at(store):
    store.add(Task(description="First", status=Status.PENDING))
    store.add(Task(description="Second", status=Status.PENDING))
    tasks = store.list()
    assert len(tasks) == 2
    assert tasks[0].description == "First"
    assert tasks[1].description == "Second"


def test_update_persists_changes(store):
    task = store.add(Task(description="Buy milk", status=Status.PENDING))
    task.status = Status.COMPLETED
    store.update(task)
    result = store.get(task.id)
    assert result.status == Status.COMPLETED


def test_delete_removes_task(store):
    task = store.add(Task(description="Buy milk", status=Status.PENDING))
    store.delete(task.id)
    assert store.get(task.id) is None


def test_id_not_reused_after_deletion(store):
    task1 = store.add(Task(description="First", status=Status.PENDING))
    store.add(Task(description="Second", status=Status.PENDING))
    store.delete(task1.id)
    task3 = store.add(Task(description="Third", status=Status.PENDING))
    assert task3.id == 3


def test_tasks_persist_across_reinitialisation(tmp_path):
    store1 = JsonStorageBackend(data_dir=tmp_path)
    store1.add(Task(description="Persisted task", status=Status.PENDING))

    store2 = JsonStorageBackend(data_dir=tmp_path)
    result = store2.get(1)
    assert result is not None
    assert result.description == "Persisted task"


# ── M5 Wave 2: storage hardening — corruption & access errors ─────────────────

# Root bypasses Unix file permissions, so chmod-based unreadable-file tests are
# meaningless when running as root.
running_as_root = hasattr(os, "geteuid") and os.geteuid() == 0
skip_if_root = pytest.mark.skipif(
    running_as_root,
    reason="chmod(0o000) does not restrict access when running as root",
)


def test_corrupt_json_raises_storage_corrupt_error_on_list(store, tmp_path):
    (tmp_path / "tasks.json").write_text("{ not valid json")
    with pytest.raises(StorageCorruptError):
        store.list()


def test_corrupt_json_raises_storage_corrupt_error_on_get(store, tmp_path):
    (tmp_path / "tasks.json").write_text("{ not valid json")
    with pytest.raises(StorageCorruptError):
        store.get(1)


def test_wrong_schema_top_level_list_raises_storage_corrupt_error(store, tmp_path):
    # Valid JSON, but the wrong shape: a list instead of the expected dict.
    (tmp_path / "tasks.json").write_text(json.dumps([]))
    with pytest.raises(StorageCorruptError):
        store.list()


def test_wrong_schema_missing_keys_raises_storage_corrupt_error(store, tmp_path):
    # Valid JSON object, but missing the required "next_id"/"tasks" keys.
    (tmp_path / "tasks.json").write_text(json.dumps({"foo": 1}))
    with pytest.raises(StorageCorruptError):
        store.list()


def test_wrong_schema_tasks_not_a_dict_raises_storage_corrupt_error(store, tmp_path):
    # "tasks" present but the wrong type (list, not dict).
    (tmp_path / "tasks.json").write_text(json.dumps({"next_id": 1, "tasks": []}))
    with pytest.raises(StorageCorruptError):
        store.list()


def test_next_id_wrong_type_raises_storage_corrupt_error(store, tmp_path):
    # "next_id" present but not an int (a string) — must be rejected at load
    # time, not blow up later in add() with a raw TypeError.
    (tmp_path / "tasks.json").write_text(json.dumps({"next_id": "x", "tasks": {}}))
    with pytest.raises(StorageCorruptError):
        store.list()


def test_next_id_bool_raises_storage_corrupt_error(store, tmp_path):
    # bool is a subclass of int, so {"next_id": true} would slip past a naive
    # isinstance(..., int) check — assert it's explicitly rejected.
    (tmp_path / "tasks.json").write_text(json.dumps({"next_id": True, "tasks": {}}))
    with pytest.raises(StorageCorruptError):
        store.list()


@skip_if_root
def test_unreadable_file_raises_storage_access_error(store, tmp_path):
    task_file = tmp_path / "tasks.json"
    task_file.write_text(json.dumps({"next_id": 1, "tasks": {}}))
    task_file.chmod(0o000)
    try:
        with pytest.raises(StorageAccessError):
            store.list()
    finally:
        # Restore perms so pytest's tmp_path cleanup can remove the file.
        task_file.chmod(0o644)


def test_write_permission_error_raises_storage_access_error(store, monkeypatch):
    # Simulate the OS refusing the write. add() first reads (no file yet → default
    # in-memory data), then the atomic _save() creates its temp file via
    # tempfile.mkstemp → boom. The OSError must surface as StorageAccessError.
    def boom(*args, **kwargs):
        raise PermissionError("write denied")

    monkeypatch.setattr("todo_cli.storage.json_store.tempfile.mkstemp", boom)
    with pytest.raises(StorageAccessError):
        store.add(Task(description="Buy milk", status=Status.PENDING))


def test_read_permission_error_raises_storage_access_error(store, tmp_path, monkeypatch):
    # Mirror the write-path test, but fail on READ so the _load OSError branch is
    # exercised regardless of UID. The chmod-based test is skip_if_root and never
    # runs in root CI; this one always does.
    (tmp_path / "tasks.json").write_text(json.dumps({"next_id": 1, "tasks": {}}))

    original_open = Path.open

    def fake_open(self, *args, **kwargs):
        mode = args[0] if args else kwargs.get("mode", "r")
        # Read mode only: no write/append/exclusive flag present.
        if not ("w" in mode or "a" in mode or "x" in mode):
            raise PermissionError("read denied")
        return original_open(self, *args, **kwargs)

    monkeypatch.setattr(Path, "open", fake_open)
    with pytest.raises(StorageAccessError):
        store.list()


def test_corrupt_task_record_raises_storage_corrupt_error(store, tmp_path):
    # Valid JSON with the correct TOP-LEVEL shape, but a single task record is
    # malformed: missing "description" and an invalid "status". Today _deserialize
    # leaks a raw KeyError/ValueError; hardening must surface StorageCorruptError.
    corrupt = {
        "next_id": 2,
        "tasks": {
            "1": {
                "id": 1,
                # "description" intentionally omitted
                "status": "bogus",  # not a valid Status value
                "due_date": None,
                "created_at": "not-an-iso-timestamp",
                "completed_at": None,
            }
        },
    }
    (tmp_path / "tasks.json").write_text(json.dumps(corrupt))

    with pytest.raises(StorageCorruptError):
        store.list()

    with pytest.raises(StorageCorruptError):
        store.get(1)


# ── #15: atomic writes — a failed save must never destroy the prior good file ──


def test_failed_write_preserves_existing_file(store, tmp_path, monkeypatch):
    # Seed a valid record so tasks.json holds something worth protecting.
    store.add(Task(description="Important task", status=Status.PENDING))

    # Seam choice: patch json.dump *as seen by the storage module* to raise on the
    # NEXT save. The in-place _save does `open("w")` (which TRUNCATES the real
    # tasks.json) and only THEN calls json.dump — so when json.dump blows up the
    # destination is already gone → original lost (RED). An atomic _save serializes
    # into a temp file and json.dump failing there leaves tasks.json untouched
    # (GREEN). This pins exactly the "destination survives a torn write" contract.
    def boom(*args, **kwargs):
        raise OSError("disk full")

    monkeypatch.setattr("todo_cli.storage.json_store.json.dump", boom)

    with pytest.raises(StorageAccessError):
        store.add(Task(description="Second task", status=Status.PENDING))

    monkeypatch.undo()

    # A brand-new backend reads straight from disk — no in-memory caching to mask
    # a truncated file. The original record must still be intact.
    fresh = JsonStorageBackend(data_dir=tmp_path)
    recovered = fresh.get(1)
    assert recovered is not None
    assert recovered.description == "Important task"

    # And the file itself must not have been left empty/truncated.
    assert (tmp_path / "tasks.json").read_text().strip() != ""


def test_successful_write_leaves_no_temp_files(store, tmp_path):
    store.add(Task(description="Buy milk", status=Status.PENDING))

    entries = sorted(p.name for p in tmp_path.iterdir())

    # Exactly the canonical file, nothing else — no `tasks.json.*`, `*.tmp`,
    # `tmp*`, or other scratch artifacts from the atomic write left behind.
    assert entries == ["tasks.json"]
