from django import forms
from accounts.models  import  UserBankAccount
from .models import Transaction
from .constants import TRANSFER_MONEY
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'amount',
            'transaction_type'
            
        ]

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account') # account value ke pop kore anlam
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True # ei field disable thakbe
        self.fields['transaction_type'].widget = forms.HiddenInput() # user er theke hide kora thakbe

    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
       
        return super().save()

class DepositForm(TransactionForm):
    def clean_amount(self): # amount field ke filter korbo
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount') # user er fill up kora form theke amra amount field er value ke niye aslam, 50
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount} $'
            )

        return amount
    
class WithdrawForm(TransactionForm):
   

    def clean_amount(self):
        account = self.account
        min_withdraw_amount = 500
        max_withdraw_amount = 20000
        balance = account.balance # 1000
        amount = self.cleaned_data.get('amount')
        
       
        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at least {min_withdraw_amount} $'
            )

        if amount > max_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at most {max_withdraw_amount} $'
            )

        if amount > balance: # amount = 5000, tar balance ache 200
            raise forms.ValidationError(
                f'You have {balance} $ in your account. '
                'You can not withdraw more than your account balance'
            )

        return amount
    

    

    

class LoanRequestForm(TransactionForm):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')

        return amount
    

class TransferMoneyForm(forms.ModelForm):
     accountNo=forms.IntegerField()
     class Meta:
          model=Transaction
          fields=['accountNo','amount']
     def __init__(self,*args,**kwargs):
          self.user_account=kwargs.pop('account')
          super().__init__(*args,**kwargs)
     def save(self,commit=True):
            self.instance.account=self.user_account
            self.instance.transection_type=TRANSFER_MONEY;
            self.instance.balance_after_transection=self.user_account.balance
            return super().save()
     def clean_amount(self):
          amount=self.cleaned_data.get('amount')
          account=self.user_account
          if account.balance<amount:
               raise forms.ValidationError(f"Your Account balance is insufficient")
          return amount
     def clean_accountNo(self):
        
        account_no = self.cleaned_data.get('accountNo')
        
        try:
           
            receiver_account = UserBankAccount.objects.get(account_no=account_no)
          
            
        except UserBankAccount.DoesNotExist:
           
            raise forms.ValidationError('Invalid receiver account number.')
        return account_no
               