module Day01

const WORDS = Dict("one" => 1, "two" => 2, "three" => 3, "four" => 4)

function digits_of(line::AbstractString)::Vector{Int}
    found = Int[]
    for (i, c) in pairs(line)
        isdigit(c) && push!(found, c - '0')
        for (w, n) in WORDS
            startswith(SubString(line, i), w) && push!(found, n)
        end
    end
    found
end

calibrate(lines) = sum(d -> 10first(d) + last(d), digits_of.(lines))

end # module
