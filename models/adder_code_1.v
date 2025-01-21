module adder(
    input a,
    input b,
    input cin,
    output sum,
    output cout
);
    assign sum = a ^ b ^ cin;  // XOR işlemi
    assign cout = (a & b) | (b & cin) | (a & cin);  // Carry-out işlemi
endmodule
