# Knowledge Tracing Dashboard

A professional, interactive dashboard showcasing Bayesian Knowledge Tracing (BKT) and Deep Knowledge Tracing (DKT) analysis results.

## 📊 Features

### 🏠 Home Page
- Overview of the project
- Quick statistics on the dataset
- Explanation of BKT vs DKT methodologies

### 📈 BKT Analysis
- **Skill Parameters**: Difficulty, learnability, guess, and slip rates
- **Skill Space Visualization**: Difficulty vs. learnability scatter plot
- **Learning Curves**: How student performance evolves with practice
- **Mastery Status**: Which skills students have mastered

### 🧠 DKT Analysis  
- **Model Performance**: AUC-ROC scores and training metrics
- **Training Progress**: Loss and validation curves over epochs
- **Individual Learner Profiles**: Specific student predictions and knowledge states
- **Knowledge Trajectories**: How estimated knowledge evolves over time
- **Prediction Accuracy**: Comparison of model predictions vs. actual performance

### 📋 Data Overview
- Dataset summary statistics
- Performance distribution analysis
- Interaction patterns and sequence length statistics
- Skill coverage breakdown
- Data quality notes and methodology explanation

## 🚀 Quick Start

### 1. Install Requirements

```bash
pip install streamlit pandas numpy matplotlib torch scikit-learn
```

Or use the included requirements.txt:

```bash
pip install -r requirements.txt
```

### 2. Extract Data from Notebook

Run the data extraction script to convert your notebook results into dashboard-ready files:

```bash
python extract_data.py
```

This will:
- Extract BKT and DKT parameters from your notebook
- Generate all visualization PNG files
- Create CSV files with results and statistics
- Store everything in the `data/` folder

### 3. Start the Dashboard

```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501` in your browser.

### 4. Navigate the Dashboard

Use the sidebar menu to switch between pages:
- **Home** (default): Overview and key statistics
- **📈 BKT Analysis**: Population-level skill characterization
- **🧠 DKT Analysis**: Individual learner predictions and trajectories
- **📋 Data Overview**: Dataset description and statistics

## 📁 Project Structure

```
dashboard/
├── app.py                          # Main Streamlit app (home page)
├── extract_data.py                 # Data extraction script
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── pages/
│   ├── 1_📈_BKT_Analysis.py       # BKT results and visualizations
│   ├── 2_🧠_DKT_Analysis.py       # DKT results and learner analysis
│   └── 3_📋_Data_Overview.py      # Dataset description and statistics
└── data/
    ├── bkt_parameters.csv          # BKT skill parameters
    ├── bkt_mastery_data.csv        # Mastery rates per skill
    ├── dkt_performance.csv         # Training metrics over epochs
    ├── dkt_accuracy_summary.csv    # Final test performance
    ├── sample_learner_profile.csv  # Example individual learner
    ├── summary_stats.csv           # Dataset overview
    ├── skill_statistics.csv        # Per-skill statistics
    ├── bkt_skill_space.png         # Difficulty vs. Learnability
    ├── bkt_learning_curves.png     # Learning trajectories
    ├── bkt_mastery.png             # Mastery rates visualization
    ├── dkt_training_curves.png     # Loss and AUC over epochs
    ├── dkt_predicted_skills.png    # Predicted P(correct) for all skills
    ├── dkt_knowledge_trajectory.png # Knowledge state evolution
    ├── performance_distribution.png # Overall performance distribution
    ├── skill_distribution.png      # Interactions per skill
    └── sequence_lengths.png        # Learner sequence length distribution
```

## 📊 Data Extraction

The `extract_data.py` script is set up to:

1. **Read from your notebook** (`custom_bkt_population.ipynb`)
2. **Extract model outputs**:
   - BKT parameters (prior, learn, guess, slip)
   - DKT performance metrics (AUC, loss curves)
   - Visualization images from both models
3. **Save to `data/` folder** in formats Streamlit can easily display

### Customizing Data Extraction

To connect the extraction script to your actual notebook results:

1. After running your notebook, the results will be saved in JSON format
2. Update the extraction functions in `extract_data.py` to parse your specific notebook outputs
3. Run `python extract_data.py` to generate the dashboard data files

## 🎨 Design Features

- **Modern & Minimalist**: Clean interface with plenty of whitespace
- **Professional Color Scheme**: Green (#1D9E75), orange (#EF9F27), blue (#2E86AB)
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Interactive Elements**: Download buttons, tabs, expandable sections
- **Information Architecture**: Logical flow from overview → detailed analysis

## 📚 Understanding the Results

### Bayesian Knowledge Tracing (BKT)

BKT models student learning as a hidden Markov model where:
- **State**: Student knows the skill (binary: learned/not learned)
- **Observations**: Correct/incorrect responses
- **Parameters**:
  - **Prior**: P(knowledge at start)
  - **Learn**: P(transition from not-learned to learned)
  - **Guess**: P(correct | not learned)
  - **Slip**: P(incorrect | learned)

### Deep Knowledge Tracing (DKT)

DKT uses an LSTM recurrent neural network to:
- Encode the entire interaction history
- Learn complex temporal patterns
- Predict performance on next attempt
- Provide student-specific predictions

### Why Both?

| Aspect | BKT | DKT |
|--------|-----|-----|
| Interpretability | ✅ Very interpretable | ⚠️ Less interpretable |
| Parameter stability | ✅ Stable with short sequences | ⚠️ Needs longer sequences |
| Complex patterns | ❌ Limited to binary states | ✅ Captures rich dynamics |
| Computational cost | ✅ Fast (EM algorithm) | ⚠️ Slower (neural network) |

## 🔧 Troubleshooting

### "Module not found" errors

```bash
pip install streamlit pandas numpy matplotlib torch scikit-learn
```

### Data files not found

Make sure you've run the extraction script:

```bash
python extract_data.py
```

### Notebook not found when extracting

Check that `custom_bkt_population.ipynb` is in the parent directory of the dashboard folder.

### Streamlit not starting

```bash
# Try specifying the file explicitly
streamlit run dashboard/app.py

# Or from within the dashboard directory
cd dashboard && streamlit run app.py
```

## 📤 Sharing Your Dashboard

### Local Sharing (USB/Network)

The entire `dashboard/` folder is self-contained. To share:

1. Copy the `dashboard/` folder to USB/cloud storage
2. Share with others (ensure they have Python + Streamlit installed)
3. They can run: `streamlit run app.py`

### Cloud Deployment

To deploy to the cloud:

1. **Streamlit Cloud** (free):
   ```
   Push to GitHub → Connect to Streamlit Cloud
   ```

2. **Heroku** (free tier discontinued):
   ```
   Use alternative platforms like Railway, Render, etc.
   ```

3. **Docker**:
   ```
   Create Dockerfile → Deploy to any cloud provider
   ```

## 📝 Next Steps

1. ✅ Install dependencies
2. ✅ Run `extract_data.py` to populate the data folder
3. ✅ Start the dashboard with `streamlit run app.py`
4. ✅ Explore your results!
5. 📤 Share with stakeholders

## 🤝 Contributing

To customize the dashboard:

1. **Edit styling**: Modify CSS in `app.py` under the `<style>` block
2. **Add new pages**: Create files in `pages/` with names starting with a number
3. **Update content**: Edit markdown text in any page file
4. **Add visualizations**: Add new plots to `extract_data.py`

## 📖 Streamlit Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Community Forum](https://discuss.streamlit.io)
- [Streamlit GitHub](https://github.com/streamlit/streamlit)

## 📧 Questions?

For issues with the dashboard itself, check Streamlit documentation. For questions about BKT/DKT methodology, consult educational data mining literature.

---

**Created**: 2024
**Project**: S3C2 Student Analysis Dashboard
