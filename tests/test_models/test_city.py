#!/usr/bin/python3

"""Unit tests for City class."""

import os
import unittest
import models
from models.city import City
from datetime import datetime
from time import sleep


class TestCityClass(unittest.TestCase):
    """Test suite for City class"""

    def test_city_attributes(self):
        """Test city attributes"""
        city = City()
        self.assertTrue(hasattr(city, "state_id"))
        self.assertTrue(hasattr(city, "name"))

    def test_subclass(self):
        """Test subclass relationship"""
        self.assertTrue(issubclass(City, models.base_model.BaseModel))


class TestCityInstantiation(unittest.TestCase):
    """Test suite for City instantiation"""

    def test_no_args_instantiates(self):
        """Test instantiation with no arguments"""
        self.assertEqual(City, type(City()))

    def test_new_instance_stored_in_objects(self):
        """Test if new instance is stored in objects"""
        self.assertIn(City(), models.storage.all().values())

    def test_id_is_public_str(self):
        """Test if id is a public string"""
        self.assertEqual(str, type(City().id))

    def test_created_at_is_public_datetime(self):
        """Test if created_at is a public datetime"""
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_is_public_datetime(self):
        """Test if updated_at is a public datetime"""
        self.assertEqual(datetime, type(City().updated_at))

    def test_state_id_is_public_class_attribute(self):
        """Test if state_id is a public class attribute"""
        cy = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(cy))
        self.assertNotIn("state_id", cy.__dict__)

    def test_name_is_public_class_attribute(self):
        """Test if name is a public class attribute"""
        cy = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(cy))
        self.assertNotIn("name", cy.__dict__)

    def test_two_cities_unique_ids(self):
        """Test if two cities have unique ids"""
        cy1 = City()
        cy2 = City()
        self.assertNotEqual(cy1.id, cy2.id)

    def test_two_cities_different_created_at(self):
        """Test if two cities have different created_at values"""
        cy1 = City()
        sleep(0.05)
        cy2 = City()
        self.assertLess(cy1.created_at, cy2.created_at)

    def test_two_cities_different_updated_at(self):
        """Test if two cities have different updated_at values"""
        cy1 = City()
        sleep(0.05)
        cy2 = City()
        self.assertLess(cy1.updated_at, cy2.updated_at)

    def test_str_representation(self):
        """Test string representation"""
        dt = datetime.today()
        dt_repr = repr(dt)
        cy = City()
        cy.id = "123456"
        cy.created_at = cy.updated_at = dt
        cystr = cy.__str__()
        self.assertIn("[City] (123456)", cystr)
        self.assertIn("'id': '123456'", cystr)
        self.assertIn("'created_at': " + dt_repr, cystr)
        self.assertIn("'updated_at': " + dt_repr, cystr)

    def test_instantiation_with_kwargs(self):
        """Test instantiation with keyword arguments"""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        cy = City(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(cy.id, "345")
        self.assertEqual(cy.created_at, dt)
        self.assertEqual(cy.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        """Test instantiation with None keyword arguments"""
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCitySave(unittest.TestCase):
    """Test suite for save method of City class"""

    @classmethod
    def setUp(self):
        """Set up class method"""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        """Tear down class method"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        """Test saving once"""
        cy = City()
        sleep(0.05)
        first_updated_at = cy.updated_at
        cy.save()
        self.assertLess(first_updated_at, cy.updated_at)

    def test_two_saves(self):
        """Test saving twice"""
        cy = City()
        sleep(0.05)
        first_updated_at = cy.updated_at
        cy.save()
        second_updated_at = cy.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        cy.save()
        self.assertLess(second_updated_at, cy.updated_at)

    def test_save_with_arg(self):
        """Test saving with argument"""
        cy = City()
        with self.assertRaises(TypeError):
            cy.save(None)

    def test_save_updates_file(self):
        """Test if save method updates file"""
        cy = City()
        cy.save()
        cyid = "City." + cy.id
        with open("file.json", "r") as f:
            self.assertIn(cyid, f.read())


class TestCityToDict(unittest.TestCase):
    """Test suite for to_dict method of City class"""

    def test_to_dict_type(self):
        """Test if to_dict returns a dictionary"""
        self.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Test if to_dict contains correct keys"""
        cy = City()
        self.assertIn("id", cy.to_dict())
        self.assertIn("created_at", cy.to_dict())
        self.assertIn("updated_at", cy.to_dict())
        self.assertIn("__class__", cy.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Test if to_dict contains added attributes"""
        cy = City()
        cy.middle_name = "Lagos"
        cy.my_number = 98
        self.assertEqual("Lagos", cy.middle_name)
        self.assertIn("my_number", cy.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Test if datetime attributes are strings in to_dict"""
        cy = City()
        cy_dict = cy.to_dict()
        self.assertEqual(str, type(cy_dict["id"]))
        self.assertEqual(str, type(cy_dict["created_at"]))
        self.assertEqual(str, type(cy_dict["updated_at"]))

    def test_to_dict_output(self):
        """Test if to_dict output is as expected"""
        dt = datetime.today()
        cy = City()
        cy.id = "123456"
        cy.created_at = cy.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(cy.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        """Test if to_dict and __dict__ are different"""
        cy = City()
        self.assertNotEqual(cy.to_dict(), cy.__dict__)

    def test_to_dict_with_arg(self):
        """Test if to_dict raises TypeError with argument"""
        cy = City()
        with self.assertRaises(TypeError):
            cy.to_dict(None)


if __name__ == '__main__':
    unittest.main()

