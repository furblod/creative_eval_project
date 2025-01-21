module adder(
    input a, b, cin,
    output sum, cout
);
    wire t1, t2, t3;

    assign t1 = a & b;
    assign t2 = b & cin;
    assign t3 = a & cin;

    assign sum = a ^ b ^ cin;
    assign cout = t1 | t2 | t3;
endmodule
