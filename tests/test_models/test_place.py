#!/usr/bin/python3

"""Unit tests for Place class."""

import os
import unittest
import models
from models.place import Place
from datetime import datetime
from time import sleep


class TestPlaceClass(unittest.TestCase):
    """Test suite for Place class"""

    def test_place_attributes(self):
        """Test place attributes"""
        place = Place()
        self.assertTrue(hasattr(place, "city_id"))
        self.assertTrue(hasattr(place, "user_id"))
        self.assertTrue(hasattr(place, "name"))
        self.assertTrue(hasattr(place, "number_rooms"))
        self.assertTrue(hasattr(place, "number_bathrooms"))
        self.assertTrue(hasattr(place, "max_guest"))
        self.assertTrue(hasattr(place, "price_by_night"))
        self.assertTrue(hasattr(place, "latitude"))
        self.assertTrue(hasattr(place, "longitude"))
        self.assertTrue(hasattr(place, "amenity_ids"))

    def test_subclass(self):
        """Test subclass relationship"""
        self.assertTrue(issubclass(Place, models.base_model.BaseModel))


class TestPlaceInstantiation(unittest.TestCase):
    """Test suite for Place instantiation"""

    def test_no_args_instantiates(self):
        """Test instantiation with no arguments"""
        self.assertEqual(Place, type(Place()))

    def test_new_instance_stored_in_objects(self):
        """Test if new instance is stored in objects"""
        self.assertIn(Place(), models.storage.all().values())

    def test_id_is_public_str(self):
        """Test if id is a public string"""
        self.assertEqual(str, type(Place().id))

    def test_created_at_is_public_datetime(self):
        """Test if created_at is a public datetime"""
        self.assertEqual(datetime, type(Place().created_at))

    def test_updated_at_is_public_datetime(self):
        """Test if updated_at is a public datetime"""
        self.assertEqual(datetime, type(Place().updated_at))

    def test_two_places_unique_ids(self):
        """Test if two places have unique ids"""
        pl1 = Place()
        pl2 = Place()
        self.assertNotEqual(pl1.id, pl2.id)

    def test_two_places_different_created_at(self):
        """Test if two places have different created_at values"""
        pl1 = Place()
        sleep(0.05)
        pl2 = Place()
        self.assertLess(pl1.created_at, pl2.created_at)

    def test_two_places_different_updated_at(self):
        """Test if two places have different updated_at values"""
        pl1 = Place()
        sleep(0.05)
        pl2 = Place()
        self.assertLess(pl1.updated_at, pl2.updated_at)

    def test_str_representation(self):
        """Test string representation"""
        dt = datetime.today()
        dt_repr = repr(dt)
        pl = Place()
        pl.id = "123456"
        pl.created_at = pl.updated_at = dt
        plstr = pl.__str__()
        self.assertIn("[Place] (123456)", plstr)
        self.assertIn("'id': '123456'", plstr)
        self.assertIn("'created_at': " + dt_repr, plstr)
        self.assertIn("'updated_at': " + dt_repr, plstr)

    def test_args_unused(self):
        """Test unused arguments"""
        pl = Place(None)
        self.assertNotIn(None, pl.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """Test instantiation with keyword arguments"""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        pl = Place(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(pl.id, "345")
        self.assertEqual(pl.created_at, dt)
        self.assertEqual(pl.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        """Test instantiation with None keyword arguments"""
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlaceSave(unittest.TestCase):
    """Test suite for save method of Place class"""

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
        pl = Place()
        sleep(0.05)
        first_updated_at = pl.updated_at
        pl.save()
        self.assertLess(first_updated_at, pl.updated_at)

    def test_two_saves(self):
        """Test saving twice"""
        pl = Place()
        sleep(0.05)
        first_updated_at = pl.updated_at
        pl.save()
        second_updated_at = pl.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        pl.save()
        self.assertLess(second_updated_at, pl.updated_at)

    def test_save_with_arg(self):
        """Test saving with argument"""
        pl = Place()
        with self.assertRaises(TypeError):
            pl.save(None)

    def test_save_updates_file(self):
        """Test if save method updates file"""
        pl = Place()
        pl.save()
        plid = "Place." + pl.id
        with open("file.json", "r") as f:
            self.assertIn(plid, f.read())


class TestPlaceToDict(unittest.TestCase):
    """Test suite for to_dict method of Place class"""

    def test_to_dict_type(self):
        """Test if to_dict returns a dictionary"""
        self.assertTrue(dict, type(Place().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Test if to_dict contains correct keys"""
        pl = Place()
        self.assertIn("id", pl.to_dict())
        self.assertIn("created_at", pl.to_dict())
        self.assertIn("updated_at", pl.to_dict())
        self.assertIn("__class__", pl.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Test if to_dict contains added attributes"""
        pl = Place()
        pl.middle_name = "Oladapo"
        pl.my_number = 26
        self.assertEqual("Oladapo", pl.middle_name)
        self.assertIn("my_number", pl.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Test if datetime attributes are strings in to_dict"""
        pl = Place()
        pl_dict = pl.to_dict()
        self.assertEqual(str, type(pl_dict["id"]))
        self.assertEqual(str, type(pl_dict["created_at"]))
        self.assertEqual(str, type(pl_dict["updated_at"]))

    def test_to_dict_output(self):
        """Test if to_dict output is as expected"""
        dt = datetime.today()
        pl = Place()
        pl.id = "123456"
        pl.created_at = pl.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(pl.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        """Test if to_dict and __dict__ are different"""
        pl = Place()
        self.assertNotEqual(pl.to_dict(), pl.__dict__)

    def test_to_dict_with_arg(self):
        """Test if to_dict raises TypeError with argument"""
        pl = Place()
        with self.assertRaises(TypeError):
            pl.to_dict(None)


if __name__ == '__main__':
    unittest.main()

