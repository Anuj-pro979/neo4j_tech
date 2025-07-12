Neo4j Perceptron Algorithm 🧠
A simple AI memory system that stores and retrieves memories using a graph database. Think of it as creating an artificial brain that can remember things and find similar memories when asked!

🎯 What Does This Do?
Imagine you're teaching a robot about animals:

Store memories: "This is a cat", "This is a dog", "Both are animals"
Connect memories: Link cats and dogs to the "animal" concept
Test memory: Ask "What's similar to a cat?" → Get back "animal" memories
Learn from usage: Track which memories are accessed most often
🧩 How It Works (Simple Explanation)
The Brain Parts:
Perception Nodes: Each memory is stored as a point in the graph
Relation Edges: Connections between related memories (like "cat" → "animal")
Embeddings: Numbers that represent what the memory "looks like" [0.8, 0.2, 0.9]
Similarity Math: Find memories with similar numbers using mathematics
The Process:
Store: Save a memory with its unique "fingerprint" (numbers)
Connect: Link related memories together
Query: When asked something, find memories with similar fingerprints
Learn: Remember which memories are used most often
🛠️ Requirements
Software Needed:
Python 3.7+
Neo4j Database (Community Edition is free)
Required Python packages
Installation Steps:
Install Neo4j Database:
Download from neo4j.com
Start Neo4j Desktop
Create a new database with password "password"
Install Python Dependencies:
bash
pip install neo4j numpy
Download This Code:
bash
git clone [your-repo-url]
cd neo4j-perceptron
🚀 Quick Start
Run the Demo:
bash
python perception_algorithm.py
What You'll See:
🚀 Starting Neo4j Perceptron Algorithm Demo
🧠 Connecting to Neo4j brain database...
✅ Connected successfully!
🧹 Clearing old memories...
✅ Brain cleared!
🎭 Creating synthetic training data...
✅ Created 3 memories with relationships
👨‍🏫 Trainer initialized!
🎓 Training started...
💾 Storing memory: visual_cat
✅ Memory visual_cat stored with 1 connections
🎉 Training completed!
🧪 Testing started...
🔍 Searching for similar memories...
🎯 Found 1 similar memories
📊 Result: 1.00 accuracy
🏆 Overall Performance: 1.00 (1.0 = perfect)
📈 Brain Statistics:
🧠 Total memories stored: 3
🔄 Average memory activations: 1.00
🎉 Demo completed successfully!
📚 Code Structure
Main Classes:
PerceptionStore - The Brain Storage
python
# Store a memory
store.store_perception(
    bundle_id="cat_memory",           # Name of the memory
    embeddings=[0.8, 0.2, 0.9],      # Numbers representing the memory
    relations=[{                      # Connections to other memories
        "target": "animal_memory", 
        "weight": 0.9
    }]
)

# Find similar memories
results = store.activate_perceptions([0.75, 0.25, 0.85])
PerceptionTrainer - The Teacher
python
# Train the system
trainer.train(training_data)

# Test the system
accuracy = trainer.test(test_queries)
🎮 Try It Yourself
Custom Training Data:
python
my_data = [
    {
        'id': 'happy_memory',
        'embedding': [0.9, 0.1, 0.8],
        'relations': [{'target': 'emotion_memory', 'weight': 0.8}]
    },
    {
        'id': 'sad_memory',
        'embedding': [0.1, 0.9, 0.2],
        'relations': [{'target': 'emotion_memory', 'weight': 0.7}]
    },
    {
        'id': 'emotion_memory',
        'embedding': [0.5, 0.5, 0.5],
        'relations': []
    }
]
Custom Test Queries:
python
my_tests = [
    {
        'name': 'happy_test',
        'embedding': [0.85, 0.15, 0.75],
        'expected': ['happy_memory']
    }
]
🔧 Configuration
Database Settings:
python
# Change these in main() function
store = PerceptionStore(
    "bolt://localhost:7687",    # Neo4j connection
    ("neo4j", "your_password")  # Username, password
)
Algorithm Parameters:
python
# In activate_perceptions() method
WHERE similarity > 0.5    # Minimum similarity threshold
LIMIT 5                   # Maximum results returned
📊 Understanding Results
Accuracy Scores:
1.0 = Perfect (found exactly what we expected)
0.8 = Good (found mostly correct results)
0.5 = Okay (found some correct results)
0.0 = Failed (couldn't find anything correct)
Similarity Scores:
0.9-1.0 = Very similar
0.7-0.9 = Quite similar
0.5-0.7 = Somewhat similar
0.0-0.5 = Not similar (filtered out)
Graph Statistics:
Nodes: Total memories stored
Activation Count: How often each memory was accessed
Confidence: How sure the system is about each memory
🚨 Troubleshooting
Common Issues:
Connection Failed:
Make sure Neo4j is running
Check if password is correct
Verify port 7687 is open
No Results Found:
Lower similarity threshold (change 0.5 to 0.3)
Check if embeddings are similar enough
Verify training data was stored correctly
Low Accuracy:
Adjust embedding vectors to be more distinct
Increase training data variety
Fine-tune similarity threshold
🎯 Next Steps
Improvements You Could Make:
Better Embeddings: Use real word embeddings instead of random numbers
More Relations: Add different types of connections (IS_A, PART_OF, etc.)
Learning: Update weights based on successful retrievals
Visualization: Create graphs showing memory connections
Real Data: Use actual text/images instead of synthetic data
Advanced Features:
Decay forgotten memories over time
Strengthen frequently used connections
Add context-aware retrieval
Implement memory consolidation
📖 Educational Value
This project teaches:

Graph Databases: How to store and query connected data
Vector Similarity: Mathematical comparison of data points
Machine Learning Basics: Training, testing, and evaluation
AI Memory Systems: How artificial brains might work
Database Design: Nodes, edges, and relationships
🤝 Contributing
Feel free to:

Add more test cases
Improve the similarity algorithm
Add visualization features
Create better documentation
Submit bug reports
📝 License
MIT License - Feel free to use this for learning and experimentation!

🙏 Acknowledgments
Neo4j for the graph database
The perceptron algorithm pioneers
Anyone learning AI and graph databases
Made with ❤️ for learning AI and graph databases

"The best way to understand AI is to build it yourself!"

