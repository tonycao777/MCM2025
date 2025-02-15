import sympy as sp

def sustainable_tourism_model():
    # Define constants and assumptions
    alpha_WD = 0.001  # ton/person Waste growth rate
    alpha_WS = 1  # TODO
    alpha_HD = 100 * 7.2  # gallon Water demand growth rate
    alpha_HS = 0.000000001  # TODO
    alpha_FD = 0.000000001  # TODO
    alpha_FS = 0.000000001  # TODO
    
    C_W = 1000  # TODO
    C_T = 70000  # Traffic capacity (assumed constant)
    initial_water_supply = 1000000 * 100  # 1 billion gallons/year

    W_Pi = 0.4  # Weight of revenue in resident satisfaction
    W_E = 0.4  # Weight of infrastructure in resident satisfaction
    W_V = 0.2  # Weight of environment in resident satisfaction

    # Define symbolic variables
    n = sp.Symbol('n')  # Number of visitors
    T = sp.Symbol('T')  # Temperature (°C)

    # Price level equation parameters
    
    epsilon_S = 0.5  # elasticity of supply
    epsilon_D = -0.3  # elasticity of demand
    c_0 = sp.ln(232/(16000 ** (1 / (epsilon_S - epsilon_D)))) # example constant value

    # Updated Price equation
    
    P = sp.exp(c_0) * n ** (1 / (epsilon_S - epsilon_D))
    
    # Business revenue
    Pi = n * P

    # Assume government spending on waste, water, and traffic
    I_W = 0
    I_H = 0
    I_T = 0

    # Waste demand
    W_D = alpha_WD * n 

    # Waste supply
    W_S = alpha_WS * sp.ln(I_W) + C_W

    # Water demand
    H_D = alpha_HD * n

    # Water supply
    H_S = initial_water_supply + alpha_HS * sp.ln(I_H)

    # Traffic demand
    F_D = alpha_FD * n
    F_S = alpha_FS * sp.ln(I_T) + C_T

    # Infrastructure metric
    ILI = ((H_D / H_S) ** 2 + (W_D / W_S) ** 2 + (F_D / F_S) ** 2) ** (1 / 2)


    # Glacier volume as a function of temperature
    Tm = 0 
    v = 1000
    t = -6
    alpha = v / sp.ln(-((t - Tm) - 31))
    V_g = alpha * sp.ln(-((T - Tm) - 31))

    # Resident satisfaction
    r_Pi = 1 / (1 + sp.exp(-0.0001 * (Pi - 45000)))
    r_E = 1 / (1 + sp.exp(20 * (ILI - 0.8)))
    r_V = 1 / (1 + sp.exp(-0.01 * (V_g - 1100)))

    Omega = W_Pi * r_Pi + W_E * r_E + W_V * r_V

    # Initialize number of visitors
    visitors_example = 16000  # Initial estimate of visitors

    # Set temperature value (e.g., T = 1)
    temperature_value = 1  # Example temperature value (1°C)

    # Create Omega function (once, outside the loop)
    Omega_func = sp.lambdify([n, T], Omega, 'numpy')  # Use numpy for lambdify

    for _ in range(100):  # Max iterations to avoid infinite loops
        # Calculate Omega based on current number of visitors
        Omega_val = Omega_func(visitors_example, temperature_value)

        # Calculate visitor satisfaction omega
        omega = W_Pi * (1 / (1 + sp.exp(0.03 * (P - 250)))) + W_E * r_E + W_V * r_V

        # Update number of visitors
        new_visitors = n * sp.exp(omega - 0.8)
        
        # Update temperature based on business revenue
        G = Pi * 0.623
        try:
            temperature_value = 0.8 / sp.ln(2) * sp.ln(G)
        except ValueError:
            print("Error in calculating temperature. Check value of G.")
            break
        temperature_value = temperature_value.subs({n: visitors_example}).evalf()

        # Evaluate new_visitors expression numerically
        new_visitors_num = new_visitors.subs({n: visitors_example, T: temperature_value}).evalf()
        print(f"New Visitors: {new_visitors_num}")

        # Check for convergence
        if abs(new_visitors_num - visitors_example) < 1e-6:
            print(f"Converged to stable number of visitors: {new_visitors_num}")
            break

        # Update number of visitors for next iteration
        visitors_example = int(new_visitors_num)

    # Final calculations with numeric substitutions
    final_Omega = Omega_func(visitors_example, temperature_value)
    print(f"Final Omega: {final_Omega}")

    # Substitute for Pi and r_E with final visitors and temperature value
    final_Pi = Pi.subs(n, visitors_example).subs(T, temperature_value).evalf()
    final_r_E = r_E.subs(n, visitors_example).subs(T, temperature_value).evalf()

    return {
        "Resident Satisfaction (Omega)": final_Omega,
        "Business Revenue (Pi)": final_Pi,
        "Infrastructure Metric (r)": final_r_E,
    }

# Example usage
result = sustainable_tourism_model()
print(result)


# Glacier volume as a function of temperature
# beta = 0.2 # TODO
# Tm = 0 + 200
# v = 1000
# t = -6 + 200
# alpha = 0.2
# #C = (beta*(v**2) + alpha)/ (np.exp(beta*(Tm)**2 - beta*((t - Tm))))
# C = v**2 + alpha*(t**2 - 2*Tm*t)
# alpha = 0.2
# beta = 0.2
# T = -5 + 200
# #V_g = np.sqrt((1 / beta) * (C* np.exp(beta * ((Tm **2) - (T - Tm)**2)) - alpha))
# # Define the range of temperatures (in Celsius)
# T_range = np.linspace(-10, 10, 100)  # Temperature range from -10°C to 10°C
# print(C)
# # Calculate glacier volume (V_g) for each temperature
# #V_g_values = np.sqrt((1 / beta) * (C * np.exp(beta * (Tm**2 - (T_range - Tm)**2)) - alpha))
# V = np.sqrt(C - alpha*(T_range**2 - 2*Tm*T_range))

# # Plot the results
# plt.plot(T_range, V, label='Glacier Volume')
# plt.xlabel("Temperature (°C)")
# plt.ylabel("Glacier Volume (V)")
# plt.title("Glacier Volume as a Function of Temperature")
# plt.grid(True)
# plt.legend()
# plt.show()

# beta = 0.1 # TODO
# Tm = 0 
# v = 1000
# t = -6
# alpha = v / sp.log(-(t - 30))
# print(alpha)
# #V_g = sp.sqrt(1 / beta * (C* sp.exp(-2 * beta * (0.5 * T**2 - Tm * T)) - alpha))
# T = 0
# V_g = alpha * sp.log(-(T-31))
# print(V_g)