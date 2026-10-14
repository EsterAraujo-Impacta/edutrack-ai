import unittest
from services.subjects_service import (
    list_subjects,
    create_subject,
    delete_subject,
    count_active_subjects,
    reset_local_data
)

class TestSubjectsIntegration(unittest.TestCase):
    def setUp(self):
        reset_local_data()

    def test_full_subject_lifecycle(self):
        # 1. Checa estado inicial do dashboard
        initial_active = count_active_subjects()
        
        # 2. Cadastro de nova disciplina (simula submissão do formulário do Streamlit)
        new_subject = create_subject(
            name="Redes de Computadores",
            code="RC-04",
            professor="Prof. Ricardo",
            semester="2026.2",
            workload_hours=80,
            status="active",
            color="#EF4444"
        )
        self.assertIsNotNone(new_subject["id"])
        
        # 3. Verifica incremento no Dashboard
        self.assertEqual(count_active_subjects(), initial_active + 1)
        
        # 4. Verifica listagem com filtros
        filtered = list_subjects(status="active", semester="2026.2")
        names = [s["name"] for s in filtered]
        self.assertIn("Redes de Computadores", names)
        
        # 5. Exclusão de disciplina
        del_result = delete_subject(new_subject["id"])
        self.assertTrue(del_result)
        self.assertEqual(count_active_subjects(), initial_active)

if __name__ == "__main__":
    unittest.main()
