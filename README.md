# HUMA-SDK - Python Package for HUMA-API

Huma-SDK is the Huma-API Software Development Kit (SDK) for Python, allowing developers to interact with the Huma-API services in their Python applications.

## Overview

This SDK simplifies the interaction with the HUMA-API, making it easy to integrate into your Python applications. It provides access to various modules, each with its set of functions for specific tasks.

## Modules

- **Questions**: Interact with question-related functionalities.
  - `submit_question`: Submit a question for answer calculation.
  - `check_question_status`: Retrieve the status of an answer calculation.
  - `fetch_answer`: Retrieve the calculated answer.

- **Histories**: Access historical question data.
  - `fetch_history`: Retrieve a list of historical questions.
  - `fetch_history_data`: Retrieve detailed data for a historical question.
  - `submit_history_visual`: Initiate the transformation of historical question data into a file format.
  - `check_history_visual_status`: Check the status of the visual conversion process.
  - `fetch_history_visual_result`: Retrieve the outcome of a visual conversion.

- **Subscribes**: Manage subscriptions to specific questions.
  - `fetch_subscribes`: Retrieve a list of subscribed questions.
  - `create_subscribe`: Subscribe to a question.
  - `fetch_subscribed_status`: Get the subscription status of a question.
  - `fetch_subscribe_data`: Retrieve detailed data for a subscribed question.
  - `delete_subscribe`: Unsubscribe from a question.

- **Favorites**: Manage favorite questions.
  - `fetch_favorites`: Retrieve a list of favorite questions.
  - `create_favorite`: Mark a question as a favorite.
  - `fetch_favorite_data`: Retrieve detailed data for a favorite question.
  - `delete_favorite`: Remove a question from favorites.

- **Quicklinks**: Access categorized quicklinks for question submission.
  - `fetch_quicklinks`: Enables users to retrieve categorized quicklinks, which are question titles that users can utilize.

- **Audits**: Retrieve audit trail logs.
  - `fetch_audits`: Retrieve audit trail logs.

- **Aliases**: Manage aliases for rules.
  - `fetch_aliases`: Retrieve aliases.

## Installation

TODO: Add installation instructions.

## Getting Started

TODO: Provide information on how to get started with the SDK.

## Environment

Before you start, make sure you have created a `.env` file from `sample.env` and update it with your actual credentials.