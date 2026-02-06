## Create a new Zig project

1. Create a directory for the project: 
```bash
mkdir <project_name>
```

2. Initialize the project:
```bash
cd <project_name> && zig init
```


## Edit source files

Once the project is initialised, source files are located in the `src` directory within `<project_name>`.


## Build

The build script is `build.zig`. Running `zig build` within `<project_name>` should build the project. The output can be found in `<project_name/zig-out>`. 
