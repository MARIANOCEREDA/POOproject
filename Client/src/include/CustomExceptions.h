#include <iostream>

#if !defined(EXCEPTIONS_H)
#define EXCEPTIONS_H

namespace CustomExceptions
{
    class InputError : public std::exception
    {
        public:
            const char* what() const noexcept override
            {
                return "Entrada inválida.";
            }
    };

    class ErrorSelection : public std::exception
    {
        public:
            const char* what() const noexcept override
            {
                return "Debe ingresar un numero entre 1 y 8.";
            }
    };
};


#endif // MACRO


