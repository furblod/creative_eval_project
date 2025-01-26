module Verilog_2bit_adder (a, b, cin)
    input [0:a-1] a, b;
    input [0:cin] cin;
    output reg [0:sum] sum, cout;
    wire [0:sum, 0:cout] cout_diff;
    assign cout_diff = a ^ b ^ cin;
    assign sum = a & b | a & cin | b & cin;
endmodule