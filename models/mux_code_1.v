module mux_2to1 (
    input a,  // İlk giriş
    input b,  // İkinci giriş
    input sel, // Seçici sinyal
    output y   // Çıkış
);
    assign y = (sel) ? b : a;
endmodule
