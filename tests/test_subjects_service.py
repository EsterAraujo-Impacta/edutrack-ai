import unittest
from services.subjects_service import (
    list_subjects,
    get_subject,
    create_subject,
    update_subject,
    delete_subject,
    count_active_subjects,
    reset_local_data
)

class TestSubjectsService(unittest.TestCase):
    def setUp(self):
        reset_local_data()

    def test_list_subjects(self):
        subjects = list_subjects()
        self.assertGreaterEqual(len(subjects), 2)
        self.assertEqual(subjects[0]["name"], "Innovation Lab")

    def test_filter_by_status(self):
        actives = list_subjects(status="active")
        self.assertTrue(all(s["status"] == "active" for s in actives))

    def test_create_subject_success(self):
        initial_count = count_active_subjects()
        new_sub = create_subject(
            name="Banco de Dados",
            semester="2026.2",
            code="BD-03",
            professor="Prof. Fernando",
            workload_hours=80
        )
        self.assertIsNotNone(new_sub["id"])
        self.assertEqual(new_sub["name"], "Banco de Dados")
        self.assertEqual(count_active_subjects(), initial_count + 1)

    def test_create_subject_validation(self):
        with self.assertRaises(ValueError):
            create_subject(name="", semester="2026.2")
        with self.assertRaises(ValueError):
            create_subject(name="Matemática", semester="")

    def test_update_subject(self):
        updated = update_subject(1, professor="Prof. Carlos Alberto", workload_hours=90)
        self.assertIsNotNone(updated)
        self.assertEqual(updated["professor"], "Prof. Carlos Alberto")
        self.assertEqual(updated["workload_hours"], 90)

    def test_delete_subject(self):
        sub = create_subject(name="Para Deletar", semester="2026.2")
        sub_id = sub["id"]
        deleted = delete_subject(sub_id)
        self.assertTrue(deleted)
        self.assertIsNone(get_subject(sub_id))

if __name__ == "__main__":
    unittest.main()
