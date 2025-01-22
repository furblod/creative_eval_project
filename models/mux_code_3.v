module mux_2to1 (
    input a,
    input b,
    input sel,
    output reg y
);
    always @(*) begin
        if (sel == 1)
            y = b;
        else
            y = a;
    end
endmodule
