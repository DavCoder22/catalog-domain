import unittest
from unittest.mock import patch, MagicMock
from src.services.catalog_service import CatalogService

class TestCatalogService(unittest.TestCase):

    @patch('src.models.catalog_model.CatalogModel')
    def setUp(self, MockCatalogModel):
        # Configurar el mock del modelo
        self.mock_model = MockCatalogModel.return_value
        self.service = CatalogService()
        self.service.model = self.mock_model

    def test_get_all_items(self):
        # Configurar el comportamiento esperado del mock
        self.mock_model.get_all_items.return_value = [
            {'_id': '1', 'name': 'Item 1'},
            {'_id': '2', 'name': 'Item 2'}
        ]

        # Llamar al método que estamos probando
        items = self.service.get_all_items()

        # Verificar el resultado
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]['name'], 'Item 1')
        self.assertEqual(items[1]['name'], 'Item 2')

    def test_get_item_by_id(self):
        # Configurar el comportamiento esperado del mock
        self.mock_model.get_item_by_id.return_value = {'_id': '1', 'name': 'Item 1'}

        # Llamar al método que estamos probando
        item = self.service.get_item_by_id('1')

        # Verificar el resultado
        self.assertEqual(item['name'], 'Item 1')

    def test_add_item(self):
        # Configurar el comportamiento esperado del mock
        self.mock_model.add_item.return_value = '1'

        # Llamar al método que estamos probando
        item_id = self.service.add_item({'name': 'New Item'})

        # Verificar el resultado
        self.mock_model.add_item.assert_called_with({'name': 'New Item'})
        self.assertEqual(item_id, '1')

    def test_update_item(self):
        # Configurar el comportamiento esperado del mock
        self.mock_model.update_item.return_value = True

        # Llamar al método que estamos probando
        success = self.service.update_item('1', {'name': 'Updated Item'})

        # Verificar el resultado
        self.mock_model.update_item.assert_called_with('1', {'name': 'Updated Item'})
        self.assertTrue(success)

    def test_delete_item(self):
        # Configurar el comportamiento esperado del mock
        self.mock_model.delete_item.return_value = True

        # Llamar al método que estamos probando
        success = self.service.delete_item('1')

        # Verificar el resultado
        self.mock_model.delete_item.assert_called_with('1')
        self.assertTrue(success)

if __name__ == '__main__':
    unittest.main()
