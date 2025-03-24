# Role To Be Evaluated
Expert Project Manager who creates detailed project plans following these key principles:
- Creates task lists in markdown format
- Delegates tasks appropriately to available agents (Coder, Tester)
- Transforms markdown plans into valid XML format
- Updates project plans using the provided tools
- Ensures testing tasks are included in the plan

# Expected Behavior
Evaluate the project plan based on these criteria:

1. Plan Structure:
   - Tasks are clearly defined with descriptive names
   - Tasks break down the work into manageable pieces
   - Tasks are properly delegated to appropriate agents
   - Testing tasks are explicitly included

2. XML Format:
   - Valid XML structure following the provided format
   - Proper nesting of tasks
   - Correct use of XML tags and elements
   - Includes all required fields (name, delegatedTo, description)
   - Follows the example XML structure

3. Agent Delegation:
   - Tasks are assigned to appropriate agents based on their roles
   - Coder tasks focus on implementation
   - Tester tasks focus on testing
   - Multiple agents are assigned when needed

4. Tool Usage:
   - Proper use of update_project_plan tool
   - Project plan is prepared for export
   - Content is properly formatted for the tool

# Desired XML Format
Make sure to pay attention to the following project plan structure:
- First tag is <project_plan>
- Second tag is <name>
- Third tag is <delegatedTo>
- Fourth tag is <description>
- Fifth tag is <tasks>
- Sixth tag is <task>
- Seventh tag is <name>
- Eighth tag is <delegatedTo>

Read the XML format below carefully, understand this structure, and evaluate whether the project plan follows this structure:
```xml
<project_plan>
    <name>Simple CLI Application in Python</name>
    <delegatedTo>
        <agent>Coder</agent>
        <agent>Tester</agent>
    </delegatedTo>
    <description>Implement basic features of the program requested by the user.</description>
    <tasks>
        <task>
            <name>Implement Feature 1</name>
            <delegatedTo>Coder</delegatedTo>
        </task>
        <task>
            <name>Implement Feature 2</name>
            <delegatedTo>Coder</delegatedTo>
        </task>
        <task>
            <name>Implement Feature 3</name>
            <delegatedTo>Coder</delegatedTo>
        </task>
        <task>
            <name>Implement Feature 4</name>
            <delegatedTo>Coder</delegatedTo>
        </task>
        <task>
            <name>Write tests for each of the features above</name>
            <delegatedTo>Coder</delegatedTo>
        </task>
        <task>
            <name>Execute tests on all implemented features to ensure that they function correctly</name>
            <delegatedTo>Tester</delegatedTo>
        </task>
    </tasks>
</project_plan>
```
