{ pkgs ? import <nixpkgs> { } }: {
  # Define the shell environment
  shell = pkgs.mkShell {
    # Specify the packages to be included in the shell
    buildInputs = with pkgs; [ python313 poetry git ];
  };
}
