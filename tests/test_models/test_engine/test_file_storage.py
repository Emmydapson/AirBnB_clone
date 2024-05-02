#!/usr/bin/python3

"""Unit tests for FileStorage class."""

import unittest
import os
import models
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorageInitialization(unittest.TestCase):
    """Test suite for initialization of the FileStorage class."""

    def test_FileStorage_instantiation_no_args(self):
        """Test instantiation with no arguments."""
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_instantiation_with_arg(self):
        """Test instantiation with arguments."""
        with self.assertRaises(TypeError):
            FileStorage("Oladapo")

    def test_FileStorage_file_path_is_private_str(self):
        """Test if __file_path is a private string."""
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def testFileStorage_objects_is_private_dict(self):
        """Test if __objects is a private dictionary."""
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storage_initializes(self):
        """Test if storage initializes properly."""
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorageMethods(unittest.TestCase):
    """Unit tests for testing methods of the FileStorage class."""

    @classmethod
    def setUpClass(cls):
        """Set up class method."""
        try:
            os.rename("file.json", "tmp")
        except FileNotFoundError:
            pass

    @classmethod
    def tearDownClass(cls):
        """Tear down class method."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        try:
            os.rename("tmp", "file.json")
        except FileNotFoundError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        """Test if all method returns a dictionary."""
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_with_arg(self):
        """Test all method with argument."""
        with self.assertRaises(TypeError):
            models.storage.all("Oladapo")

    def test_new(self):
        """Test if new method adds object to __objects."""
        bm = BaseModel()
        models.storage.new(bm)
        self.assertIn("BaseModel." + bm.id, models.storage.all().keys())
        self.assertIn(bm, models.storage.all().values())

    def test_new_with_args(self):
        """Test new method with arguments."""
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_save(self):
        """Test if save method updates file."""
        bm = BaseModel()
        models.storage.new(bm)
        models.storage.save()
        with open("file.json", "r") as f:
            self.assertIn("BaseModel." + bm.id, f.read())

    def test_save_with_arg(self):
        """Test save method with argument."""
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload_with_arg(self):
        """Test reload method with argument."""
        with self.assertRaises(TypeError):
            models.storage.reload(None)

    def test_new(self):
        """Test new method adds various objects to __objects."""
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rv)
        self.assertIn("BaseModel." + bm.id, models.storage.all().keys())
        self.assertIn(bm, models.storage.all().values())
        self.assertIn("User." + us.id, models.storage.all().keys())
        self.assertIn(us, models.storage.all().values())
        self.assertIn("State." + st.id, models.storage.all().keys())
        self.assertIn(st, models.storage.all().values())
        self.assertIn("Place." + pl.id, models.storage.all().keys())
        self.assertIn(pl, models.storage.all().values())
        self.assertIn("City." + cy.id, models.storage.all().keys())
        self.assertIn(cy, models.storage.all().values())
        self.assertIn("Amenity." + am.id, models.storage.all().keys())
        self.assertIn(am, models.storage.all().values())
        self.assertIn("Review." + rv.id, models.storage.all().keys())
        self.assertIn(rv, models.storage.all().values())

    def test_save(self):
        """Test save method updates file with various objects."""
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rv)
        models.storage.save()
        with open("file.json", "r") as f:
            file_content = f.read()
            self.assertIn("BaseModel." + bm.id, file_content)
            self.assertIn("User." + us.id, file_content)
            self.assertIn("State." + st.id, file_content)
            self.assertIn("Place." + pl.id, file_content)
            self.assertIn("City." + cy.id, file_content)
            self.assertIn("Amenity." + am.id, file_content)
            self.assertIn("Review." + rv.id, file_content)

    def test_reload(self):
        """Test reload method reloads objects from file."""
        bm = BaseModel()
        us = User()
        st = State()
        pl = Place()
        cy = City()
        am = Amenity()
        rv = Review()
        models.storage.new(bm)
        models.storage.new(us)
        models.storage.new(st)
        models.storage.new(pl)
        models.storage.new(cy)
        models.storage.new(am)
        models.storage.new(rv)
        models.storage.save()
        models.storage.reload()
        objs = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + bm.id, objs)
        self.assertIn("User." + us.id, objs)
        self.assertIn("State." + st.id, objs)
        self.assertIn("Place." + pl.id, objs)
        self.assertIn("City." + cy.id, objs)
        self.assertIn("Amenity." + am.id, objs)
        self.assertIn("Review." + rv.id, objs)


if __name__ == "__main__":
    unittest.main()

