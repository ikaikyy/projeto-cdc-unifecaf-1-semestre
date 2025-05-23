{ pkgs ? import <nixpkgs> { } }:
pkgs.mkShell {
  nativeBuildInputs = [
    (pkgs.python312.withPackages
      (ps: with ps; [ pip setuptools wheel ninja cmake ]))
    pkgs.gtk4
    pkgs.libadwaita
    pkgs.adwaita-icon-theme
    pkgs.graphene
    pkgs.gobject-introspection
    pkgs.poetry
    pkgs.cairo
    pkgs.pkg-config
    pkgs.git
  ];

  GI_TYPELIB_PATH = with pkgs;
    lib.makeSearchPath "lib/girepository-1.0" [ gtk4 libadwaita graphene ];

  shellHook = ''
    if [ ! -d "$(poetry env info --path)" ]; then
      poetry env use "${pkgs.python312}/bin/python"
    fi

    # Dynamic path detection
    export PYTHONPATH="$(poetry env info --path)/lib/python3.12/site-packages"
    echo "PYTHONPATH set to $PYTHONPATH"
  '';
}
