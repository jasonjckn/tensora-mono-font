use std::collections::HashMap;

/// Count how often each word appears, ignoring case.
fn word_freq(text: &str) -> Vec<(String, usize)> {
    let mut counts: HashMap<String, usize> = HashMap::new();
    for word in text.split_whitespace() {
        *counts.entry(word.to_lowercase()).or_insert(0) += 1;
    }
    let mut pairs: Vec<_> = counts.into_iter().collect();
    pairs.sort_by(|a, b| b.1.cmp(&a.1).then(a.0.cmp(&b.0)));
    pairs
}

fn main() {
    for (word, n) in word_freq("the cat and the hat").iter().take(3) {
        println!("{word:>6} => {n}");
    }
}
