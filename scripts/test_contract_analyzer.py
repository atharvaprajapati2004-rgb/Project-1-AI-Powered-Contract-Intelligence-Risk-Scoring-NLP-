"""
Integration test for the Contract Intelligence analysis pipeline.

This script verifies that contract text can pass through:
1. Clause extraction
2. Risk detection
3. Risk scoring
4. Final contract analysis
"""

from backend.app.analysis.contract_analyzer import analyze_contract


def main():
    sample_contract = """
    This Agreement shall automatically renew for another one-year period.

    The supplier shall have unlimited liability for all damages arising
    from the services provided.

    The parties shall maintain confidentiality of all confidential information.

    The customer shall make payment within 30 days of receiving the invoice.

    Either party may terminate this agreement with thirty days written notice.
    """

    print("=" * 60)
    print("CONTRACT ANALYSIS PIPELINE TEST")
    print("=" * 60)

    try:
        result = analyze_contract(sample_contract)

        print("\nPipeline executed successfully.\n")

        print("RESULT:")
        print("-" * 60)

        if isinstance(result, dict):
            for key, value in result.items():
                print(f"\n{key}:")
                print(value)
        else:
            print(result)

        print("\n" + "=" * 60)
        print("INTEGRATION TEST COMPLETED")
        print("=" * 60)

    except Exception as error:
        print("\nPIPELINE TEST FAILED")
        print("-" * 60)
        print(f"Error: {error}")


if __name__ == "__main__":
    main()