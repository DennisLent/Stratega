# Changes and commands
Issues with getting conan running and current fix is in an effort to get a working and compiling version on linux - ubuntu 22.04

So far changes have been made to the conanfile_linux.txt to account for changes to conan --> new version is 2.6
Changes to how conan recipes are hosted as well --> now hosted on the [conancenter](https://conan.io/)

## helpful commands
- install conan dependencies directly also making sure that the package manager is allowed to install and to install the dependencies if the binaries are not available.
```conan install deps/conanfile_linux.txt -c tools.system.package_manager:mode=install --build missing```

- show default conan profile opions
```cat ~/.conan/profiles/default```

- detect conan profile for build options
```conan profile detect```

- remove conan cache (useful when upgrading from a later version)
```rm -r ~/.conan2/{.conan.db,p}```