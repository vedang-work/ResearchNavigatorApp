"""
=========================================================
Research Navigator
Knowledge Builder
Version : 1.0
=========================================================

Creates structured Knowledge Objects following the official
schema.

This module DOES NOT

- save JSON
- load JSON
- connect database

Its only responsibility is building valid objects.
"""

from copy import deepcopy


class TopicBuilder:

    """
    Builder class used to construct Topic knowledge objects.
    """

    def __init__(self, name):

        self.topic = {

            "type": "topic",

            "identity": {

                "name": name,

                "domain": "",

                "subdomain": "",

                "difficulty": "",

                "importance": "",

                "estimated_study_time": "",

                "quality_level": "",

                "version": "1.0",

                "tags": []

            },

            "learning": {

                "overview": "",

                "why_it_matters": [],

                "intuition": "",

                "key_concepts": [],

                "prerequisites": [],

                "key_takeaways": []

            },

            "history": {

                "problem_before": "",

                "historical_motivation": "",

                "impact_on_ai": ""

            },

            "timeline": [],

            "researchers": [],

            "papers": [],

            "applications": [],

            "future": {

                "open_problems": [],

                "future_directions": []

            },

            "faq": [],

            "relationships": {

                "parent_topics": [],

                "child_topics": [],

                "related_topics": []

            }

        }

    # --------------------------------------------------

    def set_identity(self, **kwargs):

        self.topic["identity"].update(kwargs)

        return self

    # --------------------------------------------------

    def set_learning(

        self,

        overview,

        why_it_matters,

        intuition,

        key_concepts,

        prerequisites,

        key_takeaways

    ):

        self.topic["learning"] = {

            "overview": overview,

            "why_it_matters": why_it_matters,

            "intuition": intuition,

            "key_concepts": key_concepts,

            "prerequisites": prerequisites,

            "key_takeaways": key_takeaways

        }

        return self

    # --------------------------------------------------

    def set_history(

        self,

        problem_before,

        historical_motivation,

        impact_on_ai

    ):

        self.topic["history"] = {

            "problem_before": problem_before,

            "historical_motivation": historical_motivation,

            "impact_on_ai": impact_on_ai

        }

        return self

    # --------------------------------------------------

    def add_timeline(self, event):

        self.topic["timeline"].append(event)

        return self

    # --------------------------------------------------

    def add_researcher(self, researcher):

        self.topic["researchers"].append(researcher)

        return self

    # --------------------------------------------------

    def add_paper(self, paper):

        self.topic["papers"].append(paper)

        return self

    # --------------------------------------------------

    def add_application(self, application):

        self.topic["applications"].append(application)

        return self

    # --------------------------------------------------

    def add_open_problem(self, problem):

        self.topic["future"]["open_problems"].append(problem)

        return self

    # --------------------------------------------------

    def add_future_direction(self, direction):

        self.topic["future"]["future_directions"].append(direction)

        return self

    # --------------------------------------------------

    def add_faq(

        self,

        question,

        answer

    ):

        self.topic["faq"].append({

            "question": question,

            "answer": answer

        })

        return self

    # --------------------------------------------------

    def set_relationships(

        self,

        parent=[],

        child=[],

        related=[]

    ):

        self.topic["relationships"] = {

            "parent_topics": parent,

            "child_topics": child,

            "related_topics": related

        }

        return self

    # --------------------------------------------------

    def build(self):

        return deepcopy(self.topic)