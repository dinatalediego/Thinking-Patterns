from thinking_patterns.core.patterns_catalog import DocstringComoHipotesis

if __name__ == "__main__":
    p = DocstringComoHipotesis()
    print(p.aplicar({"funcion": "predict_price()", "supuesto": "relación lineal estable"}))
