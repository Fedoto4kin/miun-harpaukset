// services/searchService.js
import axios from '../axios';

export const fetchSearchSuggestions = async (query, reverse = false) => {
  try {
    const url = reverse ? 'v0/lexicon/reverse-search-suggestions/' : 'v0/lexicon/search-suggestions/';
    const response = await axios.get(url, { params: { query } });
    return response.data;
  } catch (error) {
    console.error('Error fetching search suggestions:', error);
    throw error;
  }
};

export const fetchSearchSuggestionsGrouped = async (query, reverse = false) => {
  try {
    const url = reverse ? 'v0/lexicon/reverse-search-suggestions/' : 'v0/lexicon/grouped-search-suggestions/';
    const response = await axios.get(url, { params: { query } });
    return response.data;
  } catch (error) {
    console.error('Error fetching search suggestions:', error);
    throw error;
  }
};

export const fetchWordCard = async (wordId) => {
  try {
    const response = await axios.get(`v0/lexicon/word-card/${wordId}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching word card:', error);
    throw error;
  }
};
