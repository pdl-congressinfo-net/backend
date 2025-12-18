from typing import ClassVar


class classproperty(property):
    def __get__(self, instance, owner):
        return self.fget(owner)


class Permission:
    """Base class for permission strings."""

    _resource: ClassVar[str] = ""

    _declared_actions: ClassVar[dict[str, set[str]]] = {}

    _action_hierarchy: ClassVar[dict[str, set[str]]] = {
        "manage": {"delete", "update", "create", "show", "list"},
        "delete": {"update", "show", "list"},
        "update": {"show", "list"},
        "create": {"show", "list"},
        "show": {"list"},
        "list": set(),
    }

    def __init_subclass__(cls, resource: str = "", **kwargs):
        super().__init_subclass__(**kwargs)
        cls._resource = resource
        Permission._declared_actions.setdefault(resource, set())

    @classmethod
    def satisfies(cls, *, granted: str, required: str) -> bool:
        """
        Check whether a granted permission satisfies a required permission,
        considering the action hierarchy.
        """

        granted_resource, granted_action = granted.split(":")
        required_resource, required_action = required.split(":")

        if granted_resource != required_resource:
            return False

        if granted_action == required_action:
            return True

        return required_action in cls._action_hierarchy.get(granted_action, set())

    @classmethod
    def validate_action(cls, action: str):
        declared = cls._declared_actions.get(cls._resource, set())

        if action not in declared:
            raise ValueError(
                f"Action '{action}' is not declared for resource '{cls._resource}'"
            )

        if action not in cls._action_hierarchy:
            raise ValueError(f"Invalid action: {action}")

    @classmethod
    def _get_permission(cls, action: str) -> str:
        Permission._declared_actions[cls._resource].add(action)
        return f"{cls._resource}:{action}"

    @classproperty
    def List(cls) -> str:
        return cls._get_permission("list")

    @classproperty
    def Create(cls) -> str:
        return cls._get_permission("create")

    @classproperty
    def Show(cls) -> str:
        return cls._get_permission("show")

    @classproperty
    def Update(cls) -> str:
        return cls._get_permission("update")

    @classproperty
    def Delete(cls) -> str:
        return cls._get_permission("delete")

    @classproperty
    def Manage(cls) -> str:
        return cls._get_permission("manage")


class Countries(Permission, resource="countries"):
    pass


class LocationTypes(Permission, resource="locationtypes"):
    pass


class Locations(Permission, resource="locations"):
    pass


class Events(Permission, resource="events"):
    @classproperty
    def Participate(cls) -> str:
        return cls._get_permission("participate")

    @classproperty
    def ListAll(cls) -> str:
        return cls._get_permission("listall")

    @classproperty
    def Publish(cls) -> str:
        return cls._get_permission("publish")


class EventTypes(Permission, resource="eventtypes"):
    pass


class Permissions(Permission, resource="permissions"):
    pass


class Roles(Permission, resource="roles"):
    pass


class RolePermissions(Permission, resource="rolepermissions"):
    pass


class Users(Permission, resource="users"):
    @classproperty
    def ChangePassword(cls) -> str:
        return cls._get_permission("changepassword")

    @classproperty
    def ShowMe(cls) -> str:
        return cls._get_permission("showme")


class UserPermissions(Permission, resource="userpermissions"):
    pass


class UserRoles(Permission, resource="userroles"):
    pass


class Categories(Permission, resource="categories"):
    pass


class Companies(Permission, resource="companies"):
    pass


class CompanyEmployees(Permission, resource="companyemployees"):
    pass


class Contacts(Permission, resource="contacts"):
    pass
