# everything in Ruby is an object

def syllableSplitter(string)
    cases = 0
    correct = 0

    s = "->s{s.scan(/[aiouy]+e*|e(?!d$|ly).|[td]ed|le$/).size}"

    f = eval s

    for i in 1 ... 8
            cases += 1
            if f.call(string) == i
                correct += 1
            end
    end

    p "Correct: #{correct}/#{cases}, Length: #{s.length}, Score: #{correct - s.length * 10}"
end

syllableSplitter("hello")