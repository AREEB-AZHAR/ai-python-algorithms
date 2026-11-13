tree = {
    "Path A": [15, 20],
    "Path B": [-5, 8],
    "Path C": [10, 25]
}

def alphabeta(node, depth, alpha, beta, maximizing_player):
    
    if isinstance(node, int):
        return node
    
    if maximizing_player:
        max_eval = float('-inf')
        for key, children in node.items():
           
            value = alphabeta({key: children}, depth + 1, alpha, beta, False)
            max_eval = max(max_eval, value)
            alpha = max(alpha, max_eval)
            if beta <= alpha:
                break  
        return max_eval
    else:
        
        min_eval = float('inf')
        for key, children in node.items():
            for child in children:
                value = alphabeta(child, depth + 1, alpha, beta, True)
                min_eval = min(min_eval, value)
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break  
        return min_eval

def drone_decision():
    max_values = {}
    alpha = float('-inf')
    beta = float('inf')
    for path, leaves in tree.items():
        
        min_value = alphabeta({path: leaves}, 0, alpha, beta, False)
        max_values[path] = min_value
        alpha = max(alpha, min_value)  
    
    
    best_path = max(max_values, key=max_values.get)
    print("Drone evaluation (MAX) for each path:", max_values)
    print("Best Path for Drone:", best_path, "with value:", max_values[best_path])

drone_decision()