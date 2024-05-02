#!/usr/bin/python3
"""Entry point of the command interpreter"""

import cmd
import models
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
import re


class HBNBCommand(cmd.Cmd):
    """Console class"""

    prompt = "(hbnb) "
    model_classes = ["BaseModel", "User", "State", "City", "Place", "Amenity", "Review"]

    def do_quit(self, arg):
        """Quit command to exit the console"""
        return True

    def do_EOF(self, arg):
        """Ctrl-D to exit the console"""
        return True

    def emptyline(self):
        """an empty line + ENTER shouldn't execute anything"""
        pass

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it, and prints the id"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.model_classes:
            print("** class doesn't exist **")
        else:
            obj = eval(args[0])()
            obj.save()
            print(obj.id)

    def do_show(self, arg):
        """Prints the string representation of an instance"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in self.model_classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        obj = storage.all().get(key)
        if obj is None:
            print("** no instance found **")
        else:
            print(obj)

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in self.model_classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        obj = storage.all().get(key)
        if obj is None:
            print("** no instance found **")
        else:
            del storage.all()[key]
            storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances"""
        args = arg.split()
        obj_list = []
        if len(args) == 0:
            obj_list = [str(obj) for obj in storage.all().values()]
        elif args[0] in self.model_classes:
            obj_list = [str(obj) for obj in storage.all().values() if type(obj).__name__ == args[0]]
        else:
            print("** class doesn't exist **")
            return
        print(obj_list)

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in self.model_classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        obj = storage.all().get(key)
        if obj is None:
            print("** no instance found **")
            return
        if len(args) == 2:
            print("** attribute name missing **")
            return
        if len(args) == 3:
            print("** value missing **")
            return
        setattr(obj, args[2], args[3])
        storage.save()

    def do_count(self, arg):
        """Retrieves the number of instances of a class"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in self.model_classes:
            print("** class doesn't exist **")
            return
        count = sum(1 for obj in storage.all().values() if type(obj).__name__ == args[0])
        print(count)

    def default(self, line):
        """Default behaviour if no command found"""
        match = re.match(r'(\w+)\.show\("(.+)"\)', line)
        if match:
            self.do_show(match.group(1) + " " + match.group(2))
            return
        match = re.match(r'(\w+)\.destroy\("(.+)"\)', line)
        if match:
            self.do_destroy(match.group(1) + " " + match.group(2))
            return
        print("*** Unknown syntax: {}".format(line))

    def do_custom_update(self, arg):
        """Custom Update Method"""
        if "{" not in arg or "}" not in arg:
            print("** Invalid syntax, use key value pairs within curly braces **")
            return
        arg_list = arg.split('{')
        if len(arg_list) > 2:
            print("** Invalid syntax, too many opening curly braces **")
            return
        arg = "{" + arg_list[1]
        arg_dict = eval(arg)
        if type(arg_dict) is not dict:
            print("** Invalid syntax, use key value pairs within curly braces **")
            return
        class_name = arg_list[0].strip()
        class_id = arg_dict.get("id", "")
        if class_id == "":
            print("** instance id missing **")
            return
        key = "{}.{}".format(class_name, class_id)
        obj = storage.all().get(key)
        if obj is None:
            print("** no instance found **")
            return
        for k, v in arg_dict.items():
            if k != "id":
                setattr(obj, k, v)
        storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()

