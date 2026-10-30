#if DEBUG
import SwiftUI
import UIKit

/// Screenshot-only host in an isolated checkout and a fresh simulator.
/// Production views are unmodified. All displayed records are local samples.
struct CORWebsiteCapture: View {
    private let args = ProcessInfo.processInfo.arguments
    @State private var strength = StrengthPreviewData.viewModel(.sixtyEntries)
    @State private var weight = Self.weightEngine()

    private static var didSeed = false

    init() {
        guard !Self.didSeed else { return }
        Self.didSeed = true
        let d = UserDefaults.standard
        d.set(false, forKey: "shareAnalytics")
        d.set(true, forKey: "hasSeenFirstRunTour")
        d.set("dark", forKey: "appearanceTheme")
        d.set(2200.0, forKey: "dailyCalorieGoal")
        d.set(150.0, forKey: "dailyProteinGoal")
        d.set(240.0, forKey: "dailyCarbsGoal")
        d.set(72.0, forKey: "dailyFatGoal")
        d.set(30.0, forKey: "dailyFiberGoal")
        d.set(80.0, forKey: "dailyWaterGoalOz")
        d.set(48.0, forKey: "waterIntakeOz")
        let meals = [
            Meal(name: "Eggs on sourdough", calories: 420, protein: 26, carbs: 35, fat: 19, date: Date(), imageData: nil, localUpdatedAt: .distantPast),
            Meal(name: "Chicken, rice & greens", calories: 640, protein: 48, carbs: 62, fat: 22, date: Date(), imageData: nil, localUpdatedAt: .distantPast),
            Meal(name: "Greek yogurt & berries", calories: 210, protein: 20, carbs: 26, fat: 3, date: Date(), imageData: nil, localUpdatedAt: .distantPast)
        ]
        if let encoded = try? JSONEncoder().encode(meals) { d.set(encoded, forKey: "meals") }
    }

    var body: some View {
        Group {
            if args.contains("-captureStrength") {
                NavigationStack { StrengthProgressionView(viewModel: strength) }
            } else if args.contains("-captureWeight") {
                NavigationStack { WeightDetailView(engine: weight) }
            } else if args.contains("-captureNutrition") {
                NutritionDetailView(initialMeal: Meal(name: "Grilled burger", calories: 640,
                    protein: 38, carbs: 44, fat: 35, date: Date(), imageData: nil),
                    foodImage: UIImage(named: "CORWelcomeBurger") ?? UIImage(),
                    onDone: { _ in }, onFixIssue: {}, dataSource: "AI estimate", isAIAnalyzed: true,
                    servingHistory: .none)
            } else if args.contains("-captureIngredients") {
                UnifiedProductView(data: Self.sampleProduct)
            } else if args.contains("-captureQuestions") {
                PreAnalysisQuestionsView(foodImage: UIImage(named: "CORWelcomeBurger") ?? UIImage(),
                    onAnalyze: { _, _, _ in }, onSkip: {}, seedIngredients: ["Oil", "Cheese"],
                    seedPortion: .regular, seedNotes: "Grilled, with a slice of cheese")
            } else {
                ContentView()
            }
        }
        .preferredColorScheme(.dark)
    }

    static func weightEngine() -> GoalEngine {
        let engine = GoalEngine()
        engine.currentWeightLbs = 178.2
        engine.trendWeightLbs = 178.6
        engine.startWeightLbs = 182
        engine.targetWeightLbs = 172
        engine.weightChangeThisWeek = -0.8
        engine.weightTrendEntries = [180.2, 180.1, 179.8, 180.0, 179.5, 179.6, 179.3, 179.1, 179.2, 178.9, 178.7, 178.6]
            .enumerated().map { (date: Calendar.current.date(byAdding: .day, value: ($0.offset - 11) * 2, to: Calendar.current.startOfDay(for: Date()))!, lbs: $0.element) }
        return engine
    }

    static var sampleProduct: ProductDisplayData {
        let result = FoodRiskResult(name: "Example cereal", brand: "Sample product", imageURL: nil,
            score: 0, grade: "", gradeColor: COR.accent, novaGroup: nil, isUltraProcessed: false,
            upfIndicators: [], negativeFlags: [], positiveFlags: [], additives: [],
            ingredients: OnboardingShowcase.sampleIngredients, servingSize: "40 g",
            calories: 160, protein: 4, carbs: 32, fat: 2, fiber: 3, sugar: 10, sodium: 190,
            barcode: nil, seedOils: [], detectedAllergens: [], corSays: "", capturedImage: nil)
        return ProductDisplayData(from: result)
    }
}
#endif
