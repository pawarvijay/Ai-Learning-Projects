def rrf(dense_rank, sparse_rank, k=60):
    return (1 / (k + dense_rank)) + (1 / (k + sparse_rank))

def main():
    doc = "Order ID #98214 was shipped via FedEx."
    print("Hybrid Search evaluates both semantic intent ('shipping status') and exact keyword ('98214').")
    dense_score = 0.85
    sparse_score = 1.0  # Exact keyword hit
    fusion = rrf(1, 1)
    print(f"Reciprocal Rank Fusion Score: {fusion:.4f}")

if __name__ == "__main__":
    main()
