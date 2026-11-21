$env:Path="$env:USERPROFILE\.local\share\retcomm\toolchains\cmake-clang-v1\1.0.14\bin;"+$env:Path
Set-Location C:\RecompDev\lod-recomp
& python psxrecomp\psxrecomp_cli.py rebuild --config game.toml --project-root . --build-dir build-release --no-pgo *> C:\RecompDev\lod_build.log
'done' | Out-File C:\RecompDev\lod_build_done.txt
