module adder(
    input a,  // İlk bit
    input b,  // İkinci bit
    input cin,  // Carry-in
    output sum,  // Toplam
    output cout  // Carry-out
);
    // XOR işlemi toplamı hesaplar
    assign sum = a ^ b ^ cin;

    // Carry-out, bitlerin taşıma değerlerini hesaplar
    assign cout = (a & b) | (b & cin) | (a & cin);
endmodule
