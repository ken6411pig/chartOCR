{ pkgs }: {
  deps = [
    pkgs.tesseract
    pkgs.python39
    pkgs.tesseract5
    (pkgs.tesseract5.override {
      enableLanguages = [ "eng" "chi_tra" "chi_sim" ];
    })
    # Pillow 編譯依賴
    pkgs.zlib
    pkgs.libjpeg
    pkgs.freetype
    pkgs.lcms2
    pkgs.libwebp
    pkgs.tcl
    pkgs.tk
    pkgs.harfbuzz
    pkgs.fribidi
    pkgs.pkg-config
  ];
  env = {
    LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.zlib
      pkgs.libjpeg
      pkgs.freetype
      pkgs.lcms2
      pkgs.libwebp
      pkgs.tcl
      pkgs.tk
      pkgs.harfbuzz
      pkgs.fribidi
    ];
    TESSDATA_PREFIX = "${pkgs.tesseract5}/share/tessdata";
  };
}