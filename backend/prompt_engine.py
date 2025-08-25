"""
Enhanced Prompt engineering and natural language to SQL conversion
Supports hardcoded mappings, pattern matching, and future GPT integration
"""
import re
import os
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class QueryTemplate:
    """Template class for SQL query generation"""
    
    def __init__(self, name: str, template: str, description: str, parameters: List[str] = None):
        self.name = name
        self.template = template
        self.description = description
        self.parameters = parameters or []
    
    def generate(self, **kwargs) -> str:
        """Generate SQL query from template"""
        try:
            return self.template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing parameter {e} for template {self.name}")

class PromptEngine:
    """Enhanced natural language to SQL conversion engine"""
    
    def __init__(self):
        self.hardcoded_queries = self._initialize_hardcoded_queries()
        self.table_schemas = self._initialize_table_schemas()
        self.query_templates = self._initialize_query_templates()
        self.entity_synonyms = self._initialize_entity_synonyms()
        self.operation_patterns = self._initialize_operation_patterns()
        
    # GPT integration settings (for future use)
    # self.use_gpt = os.getenv('USE_GPT_QUERY_PROCESSING', 'false').lower() == 'true'
    # self.gpt_api_key = os.getenv('OPENAI_API_KEY')
    
    def _initialize_hardcoded_queries(self) -> Dict[str, str]:
        """Initialize comprehensive hardcoded query mappings"""
        return {
            # Basic CRUD operations
            "show all citizens": "SELECT * FROM citizens ORDER BY citizen_id LIMIT 20",
            "list citizens": "SELECT citizen_id, name, age, gender FROM citizens ORDER BY name LIMIT 20",
            "count citizens": "SELECT COUNT(*) as total_citizens FROM citizens",
            "how many citizens": "SELECT COUNT(*) as total_citizens FROM citizens",
            "total citizens": "SELECT COUNT(*) as total_citizens FROM citizens",
            "citizen count": "SELECT COUNT(*) as total_citizens FROM citizens",
            "show all officers": "SELECT * FROM officers ORDER BY officer_id LIMIT 20",
            "list officers": "SELECT officer_id, name, department, rank FROM officers ORDER BY name LIMIT 20",
            "count officers": "SELECT COUNT(*) as total_officers FROM officers",
            "how many officers": "SELECT COUNT(*) as total_officers FROM officers",
            "total officers": "SELECT COUNT(*) as total_officers FROM officers",
            "show all schemes": "SELECT * FROM schemes ORDER BY scheme_id LIMIT 20",
            "list schemes": "SELECT scheme_id, scheme_name, description FROM schemes ORDER BY scheme_name LIMIT 20",
            "count schemes": "SELECT COUNT(*) as total_schemes FROM schemes",
            "how many schemes": "SELECT COUNT(*) as total_schemes FROM schemes",
            "total schemes": "SELECT COUNT(*) as total_schemes FROM schemes",
            # Analytics queries
            "citizens by gender": "SELECT gender, COUNT(*) as count FROM citizens GROUP BY gender",
            "officers by department": "SELECT department, COUNT(*) as count FROM officers GROUP BY department",
            "citizens by age group": "SELECT CASE WHEN age < 18 THEN 'Under 18' WHEN age BETWEEN 18 AND 30 THEN '18-30' WHEN age BETWEEN 31 AND 50 THEN '31-50' WHEN age BETWEEN 51 AND 65 THEN '51-65' ELSE 'Above 65' END as age_group, COUNT(*) as count FROM citizens GROUP BY age_group ORDER BY age_group",
            # System queries
            "show tables": "SELECT name FROM sqlite_master WHERE type='table'",
            "list tables": "SELECT name FROM sqlite_master WHERE type='table'",
            "database summary": "SELECT 'Citizens' as table_name, COUNT(*) as count FROM citizens UNION ALL SELECT 'Officers' as table_name, COUNT(*) as count FROM officers UNION ALL SELECT 'Schemes' as table_name, COUNT(*) as count FROM schemes",
            "data overview": "SELECT 'Citizens' as table_name, COUNT(*) as count FROM citizens UNION ALL SELECT 'Officers' as table_name, COUNT(*) as count FROM officers UNION ALL SELECT 'Schemes' as table_name, COUNT(*) as count FROM schemes",
            # Statistical queries
            "average age": "SELECT AVG(age) as average_age FROM citizens",
            "oldest citizen": "SELECT name, age FROM citizens WHERE age = (SELECT MAX(age) FROM citizens)",
            "youngest citizen": "SELECT name, age FROM citizens WHERE age = (SELECT MIN(age) FROM citizens)",
        }
        # def _initialize_hardcoded_queries(self) -> Dict[str, str]:
        #     """No hardcoded queries; use GPT for all conversions"""
        #     return {}
    
    
    def _initialize_table_schemas(self) -> Dict[str, Dict[str, Any]]:
        """Initialize detailed table schema information"""
        return {
            "citizens": {
                "columns": ["citizen_id", "name", "age", "gender", "address", "phone", "email"],
                "primary_key": "citizen_id",
                "description": "Information about citizens in the welfare system",
                "sample_queries": [
                    "Show all citizens",
                    "Count citizens by gender", 
                    "Find citizens above age 30"
                ]
            },
            "officers": {
                "columns": ["officer_id", "name", "department", "rank", "phone", "email"],
                "primary_key": "officer_id", 
                "description": "Information about government officers",
                "sample_queries": [
                    "List all officers",
                    "Show officers by department",
                    "Count officers by rank"
                ]
            },
            "schemes": {
                "columns": ["scheme_id", "scheme_name", "description", "eligibility", "benefits"],
                "primary_key": "scheme_id",
                "description": "Available welfare schemes",
                "sample_queries": [
                    "List all schemes",
                    "Show scheme details",
                    "Count total schemes"
                ]
            }
        }
    
    def _initialize_query_templates(self) -> Dict[str, QueryTemplate]:
        """Initialize reusable SQL query templates"""
        templates = {}
        
        # Basic CRUD templates
        templates['select_all'] = QueryTemplate(
            "select_all",
            "SELECT * FROM {table} ORDER BY {order_by} LIMIT {limit}",
            "Select all records from a table",
            ["table", "order_by", "limit"]
        )
        
        templates['count_records'] = QueryTemplate(
            "count_records", 
            "SELECT COUNT(*) as total_{table} FROM {table}",
            "Count total records in a table",
            ["table"]
        )
        
        templates['filter_by_column'] = QueryTemplate(
            "filter_by_column",
            "SELECT * FROM {table} WHERE {column} {operator} {value} ORDER BY {order_by} LIMIT {limit}",
            "Filter records by column value",
            ["table", "column", "operator", "value", "order_by", "limit"]
        )
        
        templates['group_by_column'] = QueryTemplate(
            "group_by_column",
            "SELECT {column}, COUNT(*) as count FROM {table} GROUP BY {column} ORDER BY count DESC",
            "Group records by column and count",
            ["table", "column"]
        )
        
        # Age-specific templates  
        templates['age_filter'] = QueryTemplate(
            "age_filter",
            "SELECT * FROM citizens WHERE age {operator} {age} ORDER BY age {sort_order} LIMIT {limit}",
            "Filter citizens by age",
            ["operator", "age", "sort_order", "limit"]
        )
        
        templates['age_range'] = QueryTemplate(
            "age_range", 
            "SELECT * FROM citizens WHERE age BETWEEN {min_age} AND {max_age} ORDER BY age LIMIT {limit}",
            "Filter citizens by age range",
            ["min_age", "max_age", "limit"]
        )
        
        return templates
    
    def _initialize_entity_synonyms(self) -> Dict[str, List[str]]:
        """Initialize synonyms for database entities"""
        return {
            "citizens": ["citizen", "people", "person", "individual", "resident", "beneficiary"],
            "officers": ["officer", "official", "staff", "employee", "personnel", "admin"],
            "schemes": ["scheme", "program", "initiative", "project", "plan", "benefit"]
        }
    
    def _initialize_operation_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize patterns for different operations"""
        return {
            "count": {
                "keywords": ["count", "how many", "number of", "total", "sum"],
                "template": "count_records",
                "chart_type": "metric"
            },
            "list": {
                "keywords": ["show", "list", "display", "get", "find", "retrieve"],
                "template": "select_all", 
                "chart_type": "table"
            },
            "filter": {
                "keywords": ["where", "with", "having", "above", "below", "greater", "less"],
                "template": "filter_by_column",
                "chart_type": "table"
            },
            "group": {
                "keywords": ["by", "group", "categorize", "breakdown"],
                "template": "group_by_column",
                "chart_type": "bar"
            },
            "compare": {
                "keywords": ["compare", "vs", "versus", "between"],
                "template": "group_by_column",
                "chart_type": "bar"
            }
        }
    
    def process_query(self, natural_language_query: str) -> Dict[str, Any]:
        """Convert natural language query to SQL using only hardcoded and pattern-matched logic"""
        try:
            from backend.db import DatabaseManager
            cleaned_query = self._clean_query(natural_language_query)
            entities = self._extract_entities(cleaned_query)
            operations = self._extract_operations(cleaned_query)
            # Try hardcoded match first
            sql_query = self._match_hardcoded_query(cleaned_query)
            method = "hardcoded"
            if not sql_query:
                # Try pattern match
                sql_query = self._pattern_match_query(cleaned_query)
                method = "pattern"
            if not sql_query:
                # Try intelligent pattern match
                sql_query = self._intelligent_pattern_match(cleaned_query, entities, operations)
                method = "intelligent_pattern"
            if not sql_query:
                return {
                    "status": "error",
                    "message": "Could not convert query to SQL. Please try rephrasing.",
                    "suggestions": self._get_intelligent_suggestions(entities, operations)
                }
            # Execute SQL and format result
            db = DatabaseManager()
            db_response = db.execute_query(sql_query)
            if db_response["status"] != "success":
                return {
                    "status": "error",
                    "message": db_response.get("message", "Database error")
                }
            # Human-readable output for count queries
            if "COUNT" in sql_query.upper():
                count = None
                for key in ["total_citizens", "total_officers", "total_schemes", "count"]:
                    if db_response["data"] and key in db_response["data"][0]:
                        count = db_response["data"][0][key]
                        break
                if count is None and db_response["data"]:
                    count = list(db_response["data"][0].values())[0]
                entity = entities[0] if entities else "records"
                return {
                    "status": "success",
                    "output": f"There are {count} {entity} in the database.",
                    "sql_query": sql_query,
                    "method": method,
                    "confidence": self._calculate_confidence(method),
                    "chart_type": "metric"
                }
            # Human-readable output for SELECT queries
            if sql_query.strip().lower().startswith("select"):
                rows = db_response.get("row_count", 0)
                entity = entities[0] if entities else "records"
                return {
                    "status": "success",
                    "output": f"Found {rows} {entity} matching your query.",
                    "sql_query": sql_query,
                    "method": method,
                    "confidence": self._calculate_confidence(method),
                    "chart_type": "table"
                }
            return {
                "status": "success",
                "output": "Query executed successfully.",
                "sql_query": sql_query,
                "method": method,
                "confidence": self._calculate_confidence(method)
            }
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "status": "error",
                "message": f"Error processing query: {str(e)}"
            }
    
    def _extract_entities(self, query: str) -> List[str]:
        """Extract database entities (tables) from query"""
        entities = []
        
        for entity, synonyms in self.entity_synonyms.items():
            for synonym in [entity] + synonyms:
                if synonym in query:
                    if entity not in entities:
                        entities.append(entity)
                    break
        
        return entities
    
    def _extract_operations(self, query: str) -> List[str]:
        """Extract operations from query"""
        operations = []
        
        for operation, config in self.operation_patterns.items():
            for keyword in config["keywords"]:
                if keyword in query:
                    if operation not in operations:
                        operations.append(operation)
                    break
        
        return operations
    
    def _intelligent_pattern_match(self, query: str, entities: List[str], operations: List[str]) -> Optional[str]:
        """Enhanced pattern matching using entities and operations"""
        
        if not entities:
            return None
        
        primary_entity = entities[0]  # Use first detected entity as primary
        
        # Count operations
        if "count" in operations:
            template = self.query_templates["count_records"]
            return template.generate(table=primary_entity)
        
        # List operations with filters
        if "list" in operations or "show" in operations:
            # Check for age filters on citizens
            if primary_entity == "citizens" and "filter" in operations:
                age_match = re.search(r'\d+', query)
                if age_match:
                    age = int(age_match.group())
                    template = self.query_templates["age_filter"]
                    
                    if any(word in query for word in ["above", "over", "greater", "more than"]):
                        return template.generate(operator=">", age=age, sort_order="DESC", limit=20)
                    elif any(word in query for word in ["below", "under", "less", "younger"]):
                        return template.generate(operator="<", age=age, sort_order="ASC", limit=20)
                    elif "between" in query:
                        # Try to extract age range
                        ages = re.findall(r'\d+', query)
                        if len(ages) >= 2:
                            min_age, max_age = sorted([int(ages[0]), int(ages[1])])
                            range_template = self.query_templates["age_range"]
                            return range_template.generate(min_age=min_age, max_age=max_age, limit=20)
            
            # Basic list operation
            template = self.query_templates["select_all"]
            primary_key = self.table_schemas[primary_entity]["primary_key"]
            return template.generate(table=primary_entity, order_by=primary_key, limit=20)
        
        # Group operations
        if "group" in operations and primary_entity in self.table_schemas:
            # Determine grouping column based on query content
            if primary_entity == "citizens":
                if "gender" in query:
                    return "SELECT gender, COUNT(*) as count FROM citizens GROUP BY gender ORDER BY count DESC"
                elif "age" in query:
                    return """
                        SELECT 
                            CASE 
                                WHEN age < 18 THEN 'Under 18'
                                WHEN age BETWEEN 18 AND 30 THEN '18-30'
                                WHEN age BETWEEN 31 AND 50 THEN '31-50'
                                WHEN age BETWEEN 51 AND 65 THEN '51-65'
                                ELSE 'Above 65'
                            END as age_group,
                            COUNT(*) as count
                        FROM citizens 
                        GROUP BY age_group 
                        ORDER BY count DESC
                    """
            elif primary_entity == "officers":
                if "department" in query:
                    return "SELECT department, COUNT(*) as count FROM officers GROUP BY department ORDER BY count DESC"
                elif "rank" in query:
                    return "SELECT rank, COUNT(*) as count FROM officers GROUP BY rank ORDER BY count DESC"
        
        return None
    
    def _format_success_response(self, sql_query: str, method: str, original: str, processed: str, entities: List[str]) -> Dict[str, Any]:
        """Format successful query response"""
        
        # Determine chart type based on query
        chart_type = "table"  # default
        
        if "COUNT(*)" in sql_query.upper():
            chart_type = "metric"
        elif "GROUP BY" in sql_query.upper():
            chart_type = "bar"
        elif any(word in sql_query.upper() for word in ["AVG", "SUM", "MAX", "MIN"]):
            chart_type = "metric"
        
        return {
            "status": "success",
            "sql_query": sql_query.strip(),
            "method": method,
            "original_query": original,
            "processed_query": processed,
            "detected_entities": entities,
            "chart_type": chart_type,
            "confidence": self._calculate_confidence(method)
        }
    
    def _calculate_confidence(self, method: str) -> float:
        """Calculate confidence score based on method used"""
        confidence_scores = {
            "hardcoded": 0.95,
            "intelligent_pattern": 0.85,
            "basic_pattern": 0.70,
            "gpt": 0.90
        }
        return confidence_scores.get(method, 0.60)
    
    def _gpt_process_query(self, query: str, entities: List[str], operations: List[str]) -> Optional[str]:
        """Call Azure OpenAI API to convert natural language to SQL"""
        import requests
        # Prepare prompt
        schema_desc = []
        for table, info in self.table_schemas.items():
            columns = ", ".join(info["columns"])
            schema_desc.append(f"{table}: {columns} - {info['description']}")
        examples = []
        sample_queries = self.get_sample_queries()
        for category, queries in sample_queries.items():
            examples.extend(queries[:2])
        prompt = f"""
You are a SQL query generator for a welfare database system.

Database Schema:
{chr(10).join(schema_desc)}

Sample Queries:
{chr(10).join(examples)}

User Query: \"{query}\"
Detected Entities: {entities}
Detected Operations: {operations}

Generate a safe SELECT-only SQL query. Include appropriate LIMIT clause.
Response format: Just the SQL query, no explanations.
"""
        # Azure OpenAI API call
        endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT')
        api_key = self.gpt_api_key
        if not endpoint or not deployment or not api_key:
            logger.error("Azure OpenAI endpoint, deployment, or API key missing")
            return None
        url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version=2023-03-15-preview"
        headers = {
            "Content-Type": "application/json",
            "api-key": api_key
        }
        data = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that generates SQL queries."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 256,
            "temperature": 0.2,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "stop": None
        }
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            sql = result["choices"][0]["message"]["content"].strip()
            # Basic validation: only allow SELECT queries
            if not sql.lower().startswith("select"):
                logger.error(f"GPT returned non-SELECT SQL: {sql}")
                return None
            return sql
        except Exception as e:
            logger.error(f"GPT API error: {e}")
            return None
    
    def prepare_gpt_prompt(self, query: str, entities: List[str], operations: List[str]) -> str:
        """Prepare a comprehensive prompt for GPT integration"""
        
        # Build schema description
        schema_desc = []
        for table, info in self.table_schemas.items():
            columns = ", ".join(info["columns"])
            schema_desc.append(f"{table}: {columns} - {info['description']}")
        
        # Get relevant examples
        examples = []
        sample_queries = self.get_sample_queries()
        for category, queries in sample_queries.items():
            examples.extend(queries[:2])  # Take 2 examples from each category
        
        prompt = f"""
Database Schema:
{chr(10).join(schema_desc)}

Sample Queries and Expected Patterns:
{chr(10).join(f"- {q}" for q in examples[:10])}

User Query: "{query}"
Detected Entities: {entities}
Detected Operations: {operations}

Instructions:
1. Generate a safe SELECT-only SQL query
2. Include appropriate WHERE clauses if filtering is needed
3. Add ORDER BY for better results presentation  
4. Always include LIMIT clause (max 50 records)
5. Use only the tables and columns from the schema above
6. Return only the SQL query without explanations

SQL Query:
"""
        return prompt.strip()
    
    def get_gpt_integration_status(self) -> Dict[str, Any]:
        """Get current GPT integration status and configuration"""
        return {
            "gpt_enabled": self.use_gpt,
            "api_key_configured": bool(self.gpt_api_key),
            "ready_for_integration": bool(self.gpt_api_key and self.use_gpt),
            "supported_features": [
                "Complex query understanding",
                "Context-aware SQL generation", 
                "Multi-table join queries",
                "Advanced filtering and aggregation"
            ],
            "environment_variables": {
                "USE_GPT_QUERY_PROCESSING": "Set to 'true' to enable GPT processing",
                "OPENAI_API_KEY": "Required for GPT integration"
            }
        }
    
    def _clean_query(self, query: str) -> str:
        """Clean and normalize the input query"""
        # Convert to lowercase and strip whitespace
        cleaned = query.lower().strip()
        
        # Remove extra spaces
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # Remove question marks and exclamation marks
        cleaned = re.sub(r'[?!]', '', cleaned)
        
        return cleaned
    
    def _match_hardcoded_query(self, query: str) -> Optional[str]:
        """Try to match query with hardcoded mappings"""
        # Direct match
        if query in self.hardcoded_queries:
            return self.hardcoded_queries[query]
        
        # Partial match
        for key, sql in self.hardcoded_queries.items():
            if key in query or query in key:
                return sql
        
        return None
    
    def _pattern_match_query(self, query: str) -> Optional[str]:
        """Try to match query using pattern recognition"""
        
        # Count patterns
        if re.search(r'\b(count|how many|number of)\b', query):
            if 'citizen' in query:
                return "SELECT COUNT(*) as total_citizens FROM citizens"
            elif 'officer' in query:
                return "SELECT COUNT(*) as total_officers FROM officers"
            elif 'scheme' in query:
                return "SELECT COUNT(*) as total_schemes FROM schemes"
        
        # Show/List patterns
        if re.search(r'\b(show|list|display|get)\b', query):
            if 'citizen' in query:
                return "SELECT * FROM citizens LIMIT 10"
            elif 'officer' in query:
                return "SELECT * FROM officers LIMIT 10"
            elif 'scheme' in query:
                return "SELECT * FROM schemes LIMIT 10"
        
        # Age-based queries
        if re.search(r'\bage\b', query):
            if re.search(r'\b(above|over|greater than)\b', query):
                age_match = re.search(r'\d+', query)
                if age_match:
                    age = age_match.group()
                    return f"SELECT * FROM citizens WHERE age > {age}"
            elif re.search(r'\b(below|under|less than)\b', query):
                age_match = re.search(r'\d+', query)
                if age_match:
                    age = age_match.group()
                    return f"SELECT * FROM citizens WHERE age < {age}"
        
        return None
    
    def _get_intelligent_suggestions(self, entities: List[str], operations: List[str]) -> List[str]:
        """Generate intelligent suggestions based on detected entities and operations"""
        suggestions = []
        
        if entities:
            primary_entity = entities[0]
            base_suggestions = [
                f"Show all {primary_entity}",
                f"Count {primary_entity}",
                f"List {primary_entity}"
            ]
            suggestions.extend(base_suggestions)
            
            # Entity-specific suggestions
            if primary_entity == "citizens":
                suggestions.extend([
                    "Show citizens above age 30",
                    "Citizens by gender",
                    "Average age of citizens"
                ])
            elif primary_entity == "officers":
                suggestions.extend([
                    "Officers by department",
                    "Show officers by rank"
                ])
        else:
            # General suggestions if no entities detected
            suggestions = self._get_query_suggestions()
        
        return suggestions[:6]  # Limit to 6 suggestions
    
    def _get_contextual_samples(self, entities: List[str]) -> Dict[str, List[str]]:
        """Get contextual sample queries based on detected entities"""
        if not entities:
            return self.get_sample_queries()
        
        samples = {}
        for entity in entities:
            if entity in self.table_schemas:
                entity_samples = self.table_schemas[entity].get("sample_queries", [])
                samples[entity.title()] = entity_samples
        
        return samples if samples else self.get_sample_queries()
    
    def _get_query_suggestions(self) -> List[str]:
        """Get general query suggestions"""
        return [
            "Show all citizens",
            "Count citizens", 
            "List officers",
            "How many schemes",
            "Show citizens above age 30",
            "Citizens by gender",
            "Officers by department",
            "Database summary"
        ]
    
    def get_sample_queries(self) -> Dict[str, List[str]]:
        """Get comprehensive categorized sample queries"""
        return {
            "Citizens": [
                "Show all citizens",
                "Count citizens", 
                "Show citizens above age 30",
                "Citizens below age 25",
                "Citizens by gender",
                "Average age of citizens",
                "Oldest citizen",
                "Citizens between age 25 and 45"
            ],
            "Officers": [
                "Show all officers",
                "Count officers",
                "List officers",
                "Officers by department",
                "Officers by rank"
            ],
            "Schemes": [
                "Show all schemes", 
                "Count schemes",
                "List available schemes",
                "Scheme details"
            ],
            "Analytics": [
                "Database summary",
                "Data overview",
                "Citizens by age group",
                "Officers by department",
                "Show tables"
            ]
        }
    
    def get_query_templates_info(self) -> Dict[str, Dict[str, Any]]:
        """Get information about available query templates"""
        template_info = {}
        for name, template in self.query_templates.items():
            template_info[name] = {
                "description": template.description,
                "parameters": template.parameters,
                "example": template.template
            }
        return template_info
    
    def get_supported_entities(self) -> Dict[str, Dict[str, Any]]:
        """Get information about supported database entities"""
        return self.table_schemas
    
    def validate_query_safety(self, sql_query: str) -> Tuple[bool, str]:
        """Validate that the generated SQL query is safe to execute"""
        sql_upper = sql_query.upper().strip()
        
        # Block dangerous operations
        dangerous_patterns = [
            'DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE', 'TRUNCATE',
            'EXEC', 'EXECUTE', 'UNION', '--', '/*', '*/', ';'
        ]
        
        for pattern in dangerous_patterns:
            if pattern in sql_upper:
                return False, f"Query contains potentially dangerous operation: {pattern}"
        
        # Ensure it's a SELECT query
        if not sql_upper.startswith('SELECT'):
            return False, "Only SELECT queries are allowed"
        
        # Check for reasonable LIMIT
        if 'LIMIT' not in sql_upper:
            return False, "Query must include a LIMIT clause for safety"
        
        return True, "Query is safe to execute"
    
    def explain_query(self, sql_query: str) -> Dict[str, Any]:
        """Provide a human-readable explanation of the SQL query"""
        explanation = {
            "query": sql_query,
            "explanation": "This query...",
            "tables_used": [],
            "operations": [],
            "filters": [],
            "sorting": None,
            "limit": None
        }
        
        # Extract tables
        tables = re.findall(r'FROM\s+(\w+)', sql_query, re.IGNORECASE)
        explanation["tables_used"] = tables
        
        # Detect operations
        if "COUNT(" in sql_query.upper():
            explanation["operations"].append("Count records")
        if "GROUP BY" in sql_query.upper():
            explanation["operations"].append("Group results")
        if "AVG(" in sql_query.upper():
            explanation["operations"].append("Calculate average")
        
        # Extract WHERE conditions
        where_match = re.search(r'WHERE\s+(.+?)(?:\s+ORDER\s+BY|\s+GROUP\s+BY|\s+LIMIT|$)', 
                               sql_query, re.IGNORECASE | re.DOTALL)
        if where_match:
            explanation["filters"].append(where_match.group(1).strip())
        
        # Extract ORDER BY
        order_match = re.search(r'ORDER\s+BY\s+(.+?)(?:\s+LIMIT|$)', sql_query, re.IGNORECASE)
        if order_match:
            explanation["sorting"] = order_match.group(1).strip()
        
        # Extract LIMIT
        limit_match = re.search(r'LIMIT\s+(\d+)', sql_query, re.IGNORECASE)
        if limit_match:
            explanation["limit"] = int(limit_match.group(1))
        
        # Generate natural language explanation
        if explanation["operations"]:
            explanation["explanation"] = f"This query {', '.join(explanation['operations']).lower()}"
        else:
            explanation["explanation"] = "This query retrieves data"
        
        if explanation["tables_used"]:
            explanation["explanation"] += f" from {', '.join(explanation['tables_used'])}"
        
        if explanation["filters"]:
            explanation["explanation"] += f" where {explanation['filters'][0]}"
        
        if explanation["sorting"]:
            explanation["explanation"] += f", sorted by {explanation['sorting']}"
        
        if explanation["limit"]:
            explanation["explanation"] += f", limited to {explanation['limit']} records"
        
        explanation["explanation"] += "."
        
        return explanation

# Enhanced global functions
prompt_engine = PromptEngine()

def convert_to_sql(query: str) -> Dict[str, Any]:
    """Convert natural language query to SQL with enhanced processing"""
    return prompt_engine.process_query(query)

def get_sample_queries() -> Dict[str, List[str]]:
    """Get categorized sample queries"""
    return prompt_engine.get_sample_queries()

def get_query_templates() -> Dict[str, Dict[str, Any]]:
    """Get available query templates"""
    return prompt_engine.get_query_templates_info()

def validate_sql_safety(sql_query: str) -> Tuple[bool, str]:
    """Validate SQL query safety"""
    return prompt_engine.validate_query_safety(sql_query)

def explain_sql_query(sql_query: str) -> Dict[str, Any]:
    """Get human-readable explanation of SQL query"""
    return prompt_engine.explain_query(sql_query)

def get_supported_entities() -> Dict[str, Dict[str, Any]]:
    """Get supported database entities information"""
    return prompt_engine.get_supported_entities()

def get_gpt_status() -> Dict[str, Any]:
    """Get GPT integration status"""
    return prompt_engine.get_gpt_integration_status()

def prepare_gpt_prompt_for_query(query: str) -> str:
    """Prepare GPT prompt for a specific query (for future use)"""
    entities = prompt_engine._extract_entities(prompt_engine._clean_query(query))
    operations = prompt_engine._extract_operations(prompt_engine._clean_query(query))
    return prompt_engine.prepare_gpt_prompt(query, entities, operations)
