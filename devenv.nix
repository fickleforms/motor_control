{
  pkgs,
  lib,
  config,
  inputs,
  ...
}:

{
  languages.python = {
    enable = true;
    uv.enable = true;
    venv.enable = true;
    venv.requirements = ''
      pymodbus
    '';
  };
}
