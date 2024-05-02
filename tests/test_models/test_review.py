#!/usr/bin/python3

"""Unittest for review.py"""

import os
import unittest
from models.review import Review
from datetime import datetime
from time import sleep


class TestReviewClass(unittest.TestCase):
    """Test suite for the Review class."""

    def test_review_attributes(self):
        """Test if Review class has the expected attributes."""
        my_review = Review()
        self.assertTrue(hasattr(my_review, "place_id"))
        self.assertTrue(hasattr(my_review, "user_id"))
        self.assertTrue(hasattr(my_review, "text"))

    def test_subclass(self):
        """Test if Review is a subclass of BaseModel."""
        self.assertTrue(issubclass(Review, BaseModel))


class TestReviewInstantiation(unittest.TestCase):
    """Test cases for Review class instantiation."""

    def test_no_args_instantiates(self):
        """Test if Review instantiates without any arguments."""
        self.assertEqual(Review, type(Review()))


    def test_instantiation_with_kwargs(self):
        """Test if Review instantiates with keyword arguments."""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        rv = Review(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(rv.id, "345")
        self.assertEqual(rv.created_at, dt)
        self.assertEqual(rv.updated_at, dt)


    def test_instantiation_with_None_kwargs(self):
        """Test if Review raises TypeError when instantiated with None kwargs."""
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReviewSave(unittest.TestCase):
    """Test cases for Review save method."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        """Tear down test environment."""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

def test_one_save(self):
        """Test if save method updates updated_at attribute."""
        rv = Review()
        sleep(0.05)
        first_updated_at = rv.updated_at
        rv.save()
        self.assertLess(first_updated_at, rv.updated_at)

    def test_save_updates_file(self):
        """Test if save method updates file storage."""
        rv = Review()
        rv.save()
        rvid = "Review." + rv.id
        with open("file.json", "r") as f:
            self.assertIn(rvid, f.read())


class TestReviewToDict(unittest.TestCase):
    """Test cases for Review to_dict method."""

    def test_to_dict_type(self):
        """Test if to_dict returns a dictionary."""
        self.assertTrue(dict, type(Review().to_dict()))


    def test_to_dict_with_arg(self):
        """Test if to_dict raises TypeError when passed an argument."""
        rv = Review()
        with self.assertRaises(TypeError):
            rv.to_dict(None)


if __name__ == '__main__':
    unittest.main()

