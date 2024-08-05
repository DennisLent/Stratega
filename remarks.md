# Changes and commands
Issues with getting conan running and current fix is in an effort to get a working and compiling version on linux - ubuntu 22.04

So far changes have been made to the conanfile_linux.txt to account for changes to conan --> new version is 2.6
Changes to how conan recipes are hosted as well --> now hosted on the [conancenter](https://conan.io/)

## helpful commands
- detect conan profile for build options
```conan profile detect```

- show default conan profile opions (you can edit it with an editor of your choice)
```cat ~/.conan/profiles/default```

- remove conan cache (useful when upgrading from a later version)
```rm -r ~/.conan2/{.conan.db,p}```

- install conan dependencies directly also making sure that the package manager is allowed to install and to install the dependencies if the binaries are not available. This creates the folder build in which all the dependencies will be created.
```conan install deps/conanfile_linux.txt -c tools.system.package_manager:mode=install --build missing --output-folder=build```

- configure the build (run with trace for debug information)
```cmake -S . -B build -DCMAKE_TOOLCHAIN_FILE=build/conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Release --trace```

- build the projects
```cmake --build build --verbose```

