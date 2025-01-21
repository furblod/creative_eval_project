module testbench;
    reg a, b, cin;           // Test için girişler
    wire sum, cout;          // Modülden gelen çıkışlar

    // Test edilen modülün bağlanması
    adder uut (
        .a(a),
        .b(b),
        .cin(cin),
        .sum(sum),
        .cout(cout)
    );

    initial begin
        $monitor("a=%b, b=%b, cin=%b -> sum=%b, cout=%b", a, b, cin, sum, cout);

        // Test durumu 1
        a = 0; b = 0; cin = 0;
        #10;

        // Test durumu 2
        a = 0; b = 1; cin = 0;
        #10;

        // Test durumu 3
        a = 1; b = 1; cin = 1;
        #10;

        // Test durumu 4
        a = 1; b = 0; cin = 1;
        #10;

        $finish; // Simülasyonu sonlandır
    end
endmodule
