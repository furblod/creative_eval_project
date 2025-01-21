module mux_2to1 (
    input a,
    input b,
    input sel,
    output y
);
    // Çıkışı bir or (|) kombinasyonu ile hesaplayın
    assign y = (~sel & a) | (sel & b);
endmodule
