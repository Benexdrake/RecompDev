$env:Path="$env:USERPROFILE\.local\share\retcomm\toolchains\cmake-clang-v1\1.0.14\bin;"+$env:Path
Set-Location C:\RecompDev\bof4-recomp
& python psxrecomp\psxrecomp_cli.py rebuild --config game.toml --project-root . --build-dir build-release --no-pgo *> C:\RecompDev\bof4_build.log
'done' | Out-File C:\RecompDev\bof4_build_done.txt
