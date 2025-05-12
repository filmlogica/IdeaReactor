def calculate_price(trend_score, complexity_level):
    """
    Calculates a smart price based on trend score and complexity.
    Prices are in dollars.
    """
    print(f"\n🧮 [Pricing Engine] Calculating price...")
    print(f"   ↳ Trend Score       : {trend_score}/10")
    print(f"   ↳ Complexity Level  : {complexity_level}")

    base_price = 4.99 + (trend_score * 1.25)
    print(f"   ➕ Base Calculation  : $4.99 + ({trend_score} × $1.25) = ${base_price:.2f}")

    if complexity_level == "simple":
        base_price *= 0.85
        print("   🟢 Simplicity Discount Applied (×0.85)")
    elif complexity_level == "complex":
        base_price *= 1.35
        print("   🔴 Complexity Surcharge Applied (×1.35)")
    else:
        print("   ⚪ No complexity modifier applied")

    final_price = round(base_price, 2)
    print(f"💰 Final Price: ${final_price}\n")
    return final_price

