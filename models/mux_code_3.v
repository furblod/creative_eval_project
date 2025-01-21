module mux_2to1 (
    input a,  // İlk giriş sinyali
    input b,  // İkinci giriş sinyali
    input sel, // Seçici sinyal
    output reg y  // Çıkış (register olarak tanımlandı)
);
    always @(*) begin
        if (sel == 1)
            y = b;
        else
            y = a;
    end
endmodule
