from backend.health.health_trend import append_score

def main():
    result = append_score()
    print("[daily-score] Appended:", result)

if __name__ == "__main__":
    main()
