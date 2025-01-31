module mux_testbench;

    reg a, b, sel;  // Girişler
    wire y;         // Çıkış

    mux_2to1 uut (  // Test edilen modül
        .a(a),
        .b(b),
        .sel(sel),
        .y(y)
    );

    initial begin
        // Test vektörleri
        $monitor("a=%b, b=%b, sel=%b -> y=%b", a, b, sel, y);

        a = 0; b = 0; sel = 0; #10;
        a = 0; b = 1; sel = 0; #10;
        a = 1; b = 0; sel = 1; #10;
        a = 1; b = 1; sel = 1; #10;

        $finish;
    end
endmodule
