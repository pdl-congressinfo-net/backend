from typing import ClassVar


class classproperty(property):
    def __get__(self, instance, owner):
        return self.fget(owner)


class Permission:
    """Base class for permission strings."""

    _resource: ClassVar[str] = ""

    def __init_subclass__(cls, resource: str = "", **kwargs):
        super().__init_subclass__(**kwargs)
        cls._resource = resource

    @classmethod
    def _get_permission(cls, action: str) -> str:
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


class Files(Permission, resource="files"):
    @classproperty
    def Upload(cls) -> str:
        return cls._get_permission("upload")

    @classproperty
    def Download(cls) -> str:
        return cls._get_permission("download")
