from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# rules
knightsAndKnaves = And(
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(AKnave, Not(AKnight)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(BKnave, Not(BKnight)),
    Biconditional(CKnight, Not(CKnave)),
    Biconditional(CKnave, Not(CKnight)),
)

# Puzzle 0
# A says "I am both a knight and a knave."
q0_aSays = And(AKnight, AKnave)
knowledge0 = And(
    knightsAndKnaves,
    Biconditional(AKnight, q0_aSays),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
q1_aSays = And(AKnave, BKnave)
knowledge1 = And(
    knightsAndKnaves,
    Biconditional(AKnight, q1_aSays),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
q2_aSays = Or(And(AKnight, BKnight), And(AKnave, BKnave))
q2_bSays = Or(And(AKnight, BKnave), And(AKnave, BKnight))
knowledge2 = And(
    knightsAndKnaves,
    Biconditional(AKnight, q2_aSays),
    Biconditional(BKnight, q2_bSays),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
q3_aClaimsKnight = Symbol("A said I am a knight")
q3_aClaimsKnave = Symbol("A said I am a knave")

q3_aSaysSomething = And(
    Or(q3_aClaimsKnight, q3_aClaimsKnave),
    Biconditional(q3_aClaimsKnight, Not(q3_aClaimsKnave)),
    Biconditional(q3_aClaimsKnave, Not(q3_aClaimsKnight)),
)
q3_bSays1 = q3_aClaimsKnave
q3_bSays2 = CKnave
q3_cSays = AKnight

knowledge3 = And(
    knightsAndKnaves,
    q3_aSaysSomething,
    Implication(AKnight, q3_aClaimsKnight),
    Implication(AKnave, q3_aClaimsKnight),
    Biconditional(BKnight, And(q3_bSays1, q3_bSays2)),
    Biconditional(BKnave, And(Not(q3_bSays1), Not(q3_bSays2))),
    Biconditional(CKnight, q3_cSays),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3),
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
