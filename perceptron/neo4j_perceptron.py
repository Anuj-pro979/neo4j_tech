"""
Neo4j Perceptron Algorithm - A Simple AI Memory System

This is a basic implementation of a perceptron-like algorithm using Neo4j graph database.
Think of it as an AI brain that can store memories (perceptions) and find similar ones.

Author: Your Name
Date: 2025
License: MIT

How it works:
1. Store memories as nodes in a graph database
2. Connect related memories with weighted edges
3. When asked a question, find similar memories using math
4. Learn from usage by tracking which memories are accessed most

Example: If you teach it about "cats" and "dogs", and later ask about "pets",
it should be able to find the related animal memories.
"""

from neo4j import GraphDatabase
import numpy as np
import random

class PerceptionStore:
    """
    This class handles storing and retrieving memories (perceptions) in Neo4j.
    Think of it as the brain's memory storage system.
    """
    
    def __init__(self, neo4j_uri, auth):
        """
        Initialize the connection to Neo4j database.
        
        Args:
            neo4j_uri (str): Database connection string (e.g., "bolt://localhost:7687")
            auth (tuple): Username and password tuple (e.g., ("neo4j", "password"))
        """
        print("🧠 Connecting to Neo4j brain database...")
        self.driver = GraphDatabase.driver(neo4j_uri, auth=auth)
        print("✅ Connected successfully!")
    
    def store_perception(self, bundle_id, embeddings, relations):
        """
        Store a new perception (memory) in the graph database.
        
        Args:
            bundle_id (str): Unique name for this memory (e.g., "visual_cat")
            embeddings (list): Numbers that represent the memory [0.8, 0.2, 0.9]
            relations (list): List of connections to other memories
        
        Example:
            store_perception("cat_memory", [0.8, 0.2, 0.9], 
                           [{"target": "animal_memory", "weight": 0.9}])
        """
        print(f"💾 Storing memory: {bundle_id}")
        
        with self.driver.session() as session:
            # Step 1: Create the memory node in the graph
            session.run("""
                CREATE (p:Perception {
                    bundle_id: $bundle_id,           // Unique ID for this memory
                    embedding: $embedding,           // The numbers that represent this memory
                    activation_count: 0,             // How many times this memory was accessed
                    confidence: 0.5                  // How confident we are about this memory
                })
            """, {'bundle_id': bundle_id, 'embedding': embeddings})
            
            # Step 2: Create connections to other memories
            for rel in relations:
                session.run("""
                    MATCH (p1:Perception {bundle_id: $bundle_id})      // Find our memory
                    MATCH (p2:Perception {bundle_id: $target})         // Find target memory
                    CREATE (p1)-[:RELATES {weight: $weight}]->(p2)     // Connect them
                """, {
                    'bundle_id': bundle_id,
                    'target': rel['target'],
                    'weight': rel['weight']  # How strong is this connection (0.0 to 1.0)
                })
        
        print(f"✅ Memory {bundle_id} stored with {len(relations)} connections")
    
    def activate_perceptions(self, query_embedding):
        """
        Find memories similar to the given query.
        This is like asking the brain "what do you remember about this?"
        
        Args:
            query_embedding (list): Numbers representing what we're looking for
            
        Returns:
            list: List of similar memories with their similarity scores
        """
        print("🔍 Searching for similar memories...")
        
        with self.driver.session() as session:
            # Use mathematical similarity to find matching memories
            result = session.run("""
                MATCH (p:Perception)
                WITH p, 
                     // Calculate similarity using dot product (mathematical similarity)
                     reduce(dot = 0.0, i IN range(0, size(p.embedding)-1) | 
                           dot + p.embedding[i] * $query[i]) as similarity
                WHERE similarity > 0.5                                   // Only get good matches
                SET p.activation_count = p.activation_count + 1          // Count this access
                RETURN p.bundle_id, similarity
                ORDER BY similarity DESC                                 // Best matches first
                LIMIT 5                                                  // Only top 5 results
            """, {'query': query_embedding})
            
            # Convert database results to Python list
            memories = [{'bundle_id': r['p.bundle_id'], 'similarity': r['similarity']} 
                       for r in result]
            
            print(f"🎯 Found {len(memories)} similar memories")
            return memories
    
    def close(self):
        """Close the database connection cleanly."""
        print("🔌 Closing database connection...")
        self.driver.close()


class PerceptionTrainer:
    """
    This class handles training and testing the perception system.
    Think of it as the teacher that shows the AI what to learn.
    """
    
    def __init__(self, perception_store):
        """
        Initialize the trainer with a perception store.
        
        Args:
            perception_store (PerceptionStore): The brain storage system
        """
        self.store = perception_store
        print("👨‍🏫 Trainer initialized!")
    
    def train(self, training_data):
        """
        Train the system by storing a bunch of memories.
        
        Args:
            training_data (list): List of memories to store
        """
        print("🎓 Training started...")
        print(f"📚 Will store {len(training_data)} memories")
        
        for i, data in enumerate(training_data):
            # Store each memory one by one
            self.store.store_perception(
                bundle_id=data['id'],           # Memory name
                embeddings=data['embedding'],   # Memory numbers
                relations=data['relations']     # Memory connections
            )
            
            # Show progress every 10 memories
            if i % 10 == 0:
                print(f"📖 Stored {i+1} memories...")
        
        print("🎉 Training completed!")
    
    def test(self, test_queries):
        """
        Test how well the system can find memories.
        
        Args:
            test_queries (list): List of test questions
            
        Returns:
            float: Average accuracy score (0.0 to 1.0)
        """
        print("🧪 Testing started...")
        results = []
        
        for query in test_queries:
            print(f"❓ Testing: {query['name']}")
            
            # Ask the brain to find similar memories
            activated = self.store.activate_perceptions(query['embedding'])
            
            # Check if we got the right answer
            accuracy = self._calculate_accuracy(activated, query['expected'])
            results.append(accuracy)
            
            print(f"📊 Result: {accuracy:.2f} accuracy")
        
        # Calculate overall performance
        avg_accuracy = sum(results) / len(results)
        print(f"🏆 Overall Performance: {avg_accuracy:.2f} (1.0 = perfect)")
        return avg_accuracy
    
    def _calculate_accuracy(self, activated, expected):
        """
        Simple accuracy calculation - did we get the right answer?
        
        Args:
            activated (list): What the AI found
            expected (list): What we expected it to find
            
        Returns:
            float: 1.0 if correct, 0.0 if wrong
        """
        if not activated:
            return 0.0  # No results = wrong
        
        # Check if the best result is what we expected
        top_result = activated[0]['bundle_id']
        return 1.0 if top_result in expected else 0.0


def create_synthetic_data():
    """
    Create fake training data for testing.
    This simulates teaching the AI about cats, dogs, and animals.
    
    Returns:
        list: Training data with 3 basic memories
    """
    print("🎭 Creating synthetic training data...")
    
    # Create 3 basic memories
    training_data = [
        {
            'id': 'visual_cat',              # Memory name
            'embedding': [0.8, 0.2, 0.9],    # Numbers representing "cat"
            'relations': []                   # Connections (added later)
        },
        {
            'id': 'visual_dog',
            'embedding': [0.7, 0.3, 0.8],    # Numbers representing "dog"
            'relations': []
        },
        {
            'id': 'visual_animal',
            'embedding': [0.6, 0.4, 0.7],    # Numbers representing "animal"
            'relations': []
        }
    ]
    
    # Add relationships: cats and dogs are both animals
    training_data[0]['relations'] = [{'target': 'visual_animal', 'weight': 0.9}]  # Cat -> Animal
    training_data[1]['relations'] = [{'target': 'visual_animal', 'weight': 0.8}]  # Dog -> Animal
    
    print("✅ Created 3 memories with relationships")
    return training_data

def create_test_queries():
    """
    Create test questions to see if the AI learned correctly.
    
    Returns:
        list: Test queries that should find specific memories
    """
    print("❓ Creating test queries...")
    
    return [
        {
            'name': 'cat_query',
            'embedding': [0.75, 0.25, 0.85],    # Numbers similar to cat
            'expected': ['visual_cat']            # Should find cat memory
        },
        {
            'name': 'dog_query', 
            'embedding': [0.65, 0.35, 0.75],    # Numbers similar to dog
            'expected': ['visual_dog']            # Should find dog memory
        },
        {
            'name': 'animal_query',
            'embedding': [0.55, 0.45, 0.65],    # Numbers similar to animal
            'expected': ['visual_animal']         # Should find animal memory
        }
    ]

def main():
    """
    Main function that runs the entire demonstration.
    This is like the control center that coordinates everything.
    """
    print("🚀 Starting Neo4j Perceptron Algorithm Demo")
    print("=" * 50)
    
    # Step 1: Setup the brain storage system
    store = PerceptionStore("bolt://localhost:7687", ("neo4j", "password"))
    trainer = PerceptionTrainer(store)
    
    try:
        # Step 2: Clear any old memories (fresh start)
        print("🧹 Clearing old memories...")
        with store.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        print("✅ Brain cleared!")
        
        # Step 3: Create training and test data
        training_data = create_synthetic_data()
        test_queries = create_test_queries()
        
        # Step 4: Train the system
        print("\n" + "=" * 50)
        trainer.train(training_data)
        
        # Step 5: Test the system
        print("\n" + "=" * 50)
        accuracy = trainer.test(test_queries)
        
        # Step 6: Show brain statistics
        print("\n" + "=" * 50)
        print("📈 Brain Statistics:")
        with store.driver.session() as session:
            stats = session.run("""
                MATCH (n:Perception) 
                RETURN count(n) as nodes, 
                       avg(n.activation_count) as avg_activations
            """).single()
            
            print(f"🧠 Total memories stored: {stats['nodes']}")
            print(f"🔄 Average memory activations: {stats['avg_activations']:.2f}")
        
        print("\n" + "=" * 50)
        print("🎉 Demo completed successfully!")
        
        # Interpretation guide
        print("\n📖 How to interpret results:")
        print("- Accuracy 1.0 = Perfect (AI found exactly what we expected)")
        print("- Accuracy 0.0 = Failed (AI couldn't find the right memory)")
        print("- Activation count = How many times each memory was accessed")
        
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        print("💡 Make sure Neo4j is running and credentials are correct")
    
    finally:
        # Always close the connection
        store.close()
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()
