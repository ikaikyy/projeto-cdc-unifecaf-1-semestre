{ pkgs ? import <nixpkgs> { } }:
pkgs.mkShell {
  nativeBuildInputs = [
    (pkgs.python312.withPackages (ps: with ps; [ pip setuptools ]))
    pkgs.poetry
    pkgs.git
  ];

  shellHook = ''
    if [ ! -d "$(poetry env info --path)" ]; then
      poetry env use "${pkgs.python312}/bin/python"
    fi

    # Dynamic path detection
    export PYTHONPATH="$(poetry env info --path)/lib/python3.12/site-packages"
    echo "PYTHONPATH set to $PYTHONPATH"
  '';
}
