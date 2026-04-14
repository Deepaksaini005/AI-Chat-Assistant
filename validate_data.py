import json
import re
from typing import Dict, List, Tuple

class DataValidator:
    """Validate and analyze training dataset quality"""
    
    def __init__(self, data_file="chat_history.json"):
        self.data_file = data_file
        self.data = self._load_data()
        self.issues = []
        
    def _load_data(self) -> List[Dict]:
        """Load data from JSON file"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading data: {e}")
            return []
    
    def validate_structure(self) -> bool:
        """Check data structure validity"""
        print("\n🔍 Validating dataset structure...")
        
        for i, conversation in enumerate(self.data):
            # Check required fields
            if 'id' not in conversation:
                self.issues.append(f"Conversation {i}: missing 'id' field")
            if 'messages' not in conversation:
                self.issues.append(f"Conversation {i}: missing 'messages' field")
                continue
            
            messages = conversation['messages']
            
            # Check message structure
            if not isinstance(messages, list):
                self.issues.append(f"Conversation {i}: 'messages' is not a list")
                continue
            
            for j, msg in enumerate(messages):
                if 'role' not in msg:
                    self.issues.append(f"Conversation {i}, message {j}: missing 'role'")
                if 'content' not in msg:
                    self.issues.append(f"Conversation {i}, message {j}: missing 'content'")
        
        if self.issues:
            print(f"  ✗ Found {len(self.issues)} structural issues")
            for issue in self.issues[:5]:
                print(f"    - {issue}")
            if len(self.issues) > 5:
                print(f"    ... and {len(self.issues)-5} more")
            return False
        
        print("  ✓ All conversations have valid structure")
        return True
    
    def check_duplicates(self) -> bool:
        """Check for duplicate conversations"""
        print("\n🔄 Checking for duplicates...")
        
        seen_pairs = set()
        duplicates = []
        
        for conversation in self.data:
            messages = conversation.get('messages', [])
            # Create signature from first user and assistant messages
            if len(messages) >= 2:
                user_content = messages[0].get('content', '').strip().lower()
                asst_content = messages[1].get('content', '').strip().lower()
                pair_sig = (user_content, asst_content[:50])  # First 50 chars
                
                if pair_sig in seen_pairs:
                    duplicates.append((user_content[:50], asst_content[:50]))
                else:
                    seen_pairs.add(pair_sig)
        
        if duplicates:
            print(f"  ⚠ Found {len(duplicates)} potential duplicates (showing first 5):")
            for user, asst in duplicates[:5]:
                print(f"    User: {user}...")
                print(f"    Asst: {asst}...")
            return False
        
        print("  ✓ No duplicates found")
        return True
    
    def check_content_quality(self) -> bool:
        """Check content length and emptiness"""
        print("\n✍️  Checking content quality...")
        
        issues_found = False
        
        empty_count = 0
        short_count = 0
        long_count = 0
        
        for i, conversation in enumerate(self.data):
            for j, msg in enumerate(conversation.get('messages', [])):
                content = msg.get('content', '').strip()
                
                if not content:
                    empty_count += 1
                    self.issues.append(f"Conversation {i}, message {j}: empty content")
                elif len(content) < 3:
                    short_count += 1
                    self.issues.append(f"Conversation {i}, message {j}: too short ({len(content)} chars)")
                elif len(content) > 2000:
                    long_count += 1
                    print(f"  ⚠ Conversation {i}, message {j}: very long ({len(content)} chars), may need truncation")
        
        if empty_count > 0:
            print(f"  ✗ Found {empty_count} empty messages")
            issues_found = True
        if short_count > 0:
            print(f"  ⚠ Found {short_count} very short messages (< 3 chars)")
        
        if not issues_found and short_count == 0:
            print("  ✓ All content has reasonable length")
        
        return not (empty_count > 0)
    
    def check_language_diversity(self) -> bool:
        """Check for language diversity"""
        print("\n🌐 Checking language diversity...")
        
        roles = {'user': 0, 'assistant': 0}
        topics = {}
        
        for conversation in self.data:
            for msg in conversation.get('messages', []):
                role = msg.get('role', 'unknown')
                content = msg.get('content', '').lower()
                roles[role] = roles.get(role, 0) + 1
                
                # Identify topic
                if 'python' in content or 'code' in content:
                    topics['tech'] = topics.get('tech', 0) + 1
                elif 'hello' in content or 'hi' in content:
                    topics['greeting'] = topics.get('greeting', 0) + 1
                elif 'joke' in content:
                    topics['casual'] = topics.get('casual', 0) + 1
        
        print(f"  Role distribution: {roles}")
        print(f"  Topic distribution: {topics}")
        
        if roles.get('user', 0) == 0 or roles.get('assistant', 0) == 0:
            print("  ✗ Missing user or assistant messages!")
            return False
        
        print("  ✓ Good role and topic diversity")
        return True
    
    def get_statistics(self) -> Dict:
        """Get comprehensive dataset statistics"""
        print("\n📊 Computing statistics...")
        
        total_conversations = len(self.data)
        total_messages = sum(len(c.get('messages', [])) for c in self.data)
        
        # Calculate average message length
        all_lengths = []
        for c in self.data:
            for msg in c.get('messages', []):
                content = msg.get('content', '')
                all_lengths.append(len(content))
        
        avg_length = sum(all_lengths) / len(all_lengths) if all_lengths else 0
        min_length = min(all_lengths) if all_lengths else 0
        max_length = max(all_lengths) if all_lengths else 0
        
        return {
            'total_conversations': total_conversations,
            'total_messages': total_messages,
            'avg_message_length': round(avg_length, 2),
            'min_message_length': min_length,
            'max_message_length': max_length,
        }
    
    def run_validation(self) -> bool:
        """Run all validations"""
        print("="*60)
        print("🚀 TRAINING DATASET VALIDATION")
        print("="*60)
        
        if not self.data:
            print("✗ No data loaded!")
            return False
        
        print(f"\n📌 Dataset size: {len(self.data)} conversations")
        
        # Run validations
        structure_ok = self.validate_structure()
        duplicates_ok = self.check_duplicates()
        quality_ok = self.check_content_quality()
        diversity_ok = self.check_language_diversity()
        
        # Get statistics
        stats = self.get_statistics()
        print(f"\n📈 Statistics:")
        print(f"  Total conversations: {stats['total_conversations']}")
        print(f"  Total messages: {stats['total_messages']}")
        print(f"  Average message length: {stats['avg_message_length']} chars")
        print(f"  Message length range: {stats['min_message_length']} - {stats['max_message_length']} chars")
        
        # Overall assessment
        print("\n" + "="*60)
        if structure_ok and duplicates_ok and quality_ok:
            print("✓ DATASET VALIDATION PASSED")
            print("✓ Ready for training!")
            
            # Show recommendations
            if stats['total_conversations'] < 500:
                print(f"\n💡 Recommendation: Consider expanding from {stats['total_conversations']} to 500+ examples")
                print("   for better model performance. Run generate_data.py again.")
            
            print("="*60)
            return True
        else:
            print("✗ DATASET VALIDATION FAILED")
            print("✗ Please fix issues before training")
            print("="*60)
            return False


if __name__ == "__main__":
    validator = DataValidator("chat_history.json")
    success = validator.run_validation()
    exit(0 if success else 1)
