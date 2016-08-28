package cn.edu.tsinghua.thss.popcorn;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.Color;
import android.support.v4.app.FragmentActivity;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Adapter;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.lidroid.xutils.HttpUtils;
import com.lidroid.xutils.ViewUtils;
import com.lidroid.xutils.exception.HttpException;
import com.lidroid.xutils.http.RequestParams;
import com.lidroid.xutils.http.ResponseInfo;
import com.lidroid.xutils.http.callback.RequestCallBack;
import com.lidroid.xutils.http.client.HttpRequest;
import com.lidroid.xutils.view.annotation.ViewInject;
import com.lidroid.xutils.view.annotation.event.OnClick;
import com.roomorama.caldroid.CaldroidFragment;
import com.roomorama.caldroid.CaldroidListener;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

import cn.edu.tsinghua.thss.popcorn.config.Config;
import cn.edu.tsinghua.thss.popcorn.utils.SharedPreferencesUtil;


public class RepairRecordActivity extends FragmentActivity implements View.OnClickListener {

    private CaldroidFragment dialogCaldroidFragment;
    @ViewInject(R.id.repair_record_start_date)
    private EditText start_date;

    @ViewInject(R.id.repair_record_end_date)
    private EditText end_date;

    @ViewInject(R.id.repair_record_submit_passwd_btn)
    private Button submit;

    @ViewInject(R.id.lv_repair_record)
    private ListView lv;

    @ViewInject(R.id.start_date_ll)
    private LinearLayout start_date_ll;

    @ViewInject(R.id.end_date_ll)
    private LinearLayout end_date_ll;

    public  String START_DATE="";
    public  String END_DATE="";

    private JSONArray repairRecordList=null;
    RepairRecordAdapter adapter;
    private Map<String, Date> startMap;
    private Map<String, Date> endMap;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_repair_record);
        ViewUtils.inject(this);
        start_date_ll.setOnClickListener(this);
        end_date_ll.setOnClickListener(this);
        start_date.setOnClickListener(this);
        end_date.setOnClickListener(this);
        submit.setOnClickListener(this);

    }

//    start_date_ll.onInterceptTouchEvent(){

//    }
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_repair_record, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()){
            case R.id.repair_record_start_date:


                startMap = inputDate(start_date);

//                START_DATE=start_date.getText().toString();
                break;
            case  R.id.repair_record_end_date:

                endMap = inputDate(end_date);

                break;
            case R.id.repair_record_submit_passwd_btn:
                START_DATE=start_date.getText().toString();

                END_DATE=end_date.getText().toString();
                SharedPreferencesUtil.putString(this,Config.START_DAY,START_DATE);
                SharedPreferencesUtil.putString(this,Config.END_DAY,END_DATE);
                if(endMap.get(END_DATE).getTime()< startMap.get(START_DATE).getTime()){
                    new AlertDialog.Builder(this)
                            .setTitle("截止日期不能小于起始日期")
                            .setPositiveButton("知道了",null)
                            .show();
                }
                if(START_DATE.equals("")||END_DATE.equals("")){
                    new AlertDialog.Builder(RepairRecordActivity.this)
                            .setTitle("日期不能有空")
                            .setPositiveButton("确定",null)
                            .show();
//                    return;
                }
                HttpUtils http=new HttpUtils();
                http.configCurrentHttpCacheExpiry(Config.MAX_NETWORK_TIME);

                RequestParams params = new RequestParams();
                params.addQueryStringParameter("username",Config.DEBUG_USERNAME);
                params.addQueryStringParameter("access_token",Config.ACCESS_TOKEN);
                params.addQueryStringParameter("start_date",START_DATE);
                params.addQueryStringParameter("end_date",END_DATE);

                http.send(HttpRequest.HttpMethod.GET,
                        Config.REPAIR_RECORD,
                        params,
                        new RequestCallBack<String>() {
                            @Override
                            public void onSuccess(ResponseInfo<String> responseInfo) {
                                try{
                                    JSONObject jsonObject = new JSONObject(responseInfo.result);
                                    String status = jsonObject.getString("status");
                                    if(status.equals("ok")){
                                        repairRecordList=jsonObject.getJSONArray("data");
//                                        Log.e("长度","=============="+repairRecordList.length());
                                        adapter=new RepairRecordAdapter(RepairRecordActivity.this);
                                        lv.setAdapter(adapter);
                                        setListViewHeight(lv);
                                    }
                                }
                                catch (JSONException e){
                                    e.printStackTrace();
                                }
                            }

                            @Override
                            public void onFailure(HttpException e, String s) {

                            }
                        });
                break;
        }
    }

    private void setListViewHeight(ListView lv) {
        Adapter adapter=lv.getAdapter();
        if(lv==null){
            return;
        }
        int totalHeight=0;
        for(int i=0;i<adapter.getCount();i++){
            View viewItem=adapter.getView(i,null,lv);
            viewItem.measure(0,0);
            totalHeight+=viewItem.getMeasuredHeight();
        }
        ViewGroup.LayoutParams params=lv.getLayoutParams();
        params.height=totalHeight+lv.getDividerHeight()*(adapter.getCount()-1);
        lv.setLayoutParams(params);
    }


    class RepairRecordAdapter extends BaseAdapter{


        private LayoutInflater mInflater = null;

        public RepairRecordAdapter(Context context) {
            super();
            mInflater = (LayoutInflater) context
                    .getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        }
        @Override
        public int getCount() {
//            Log.e("长度2222222","=============="+returnpairRecordList.length());
            return repairRecordList.length();
        }

        @Override
        public Object getItem(int position) {
            return null;
        }

        @Override
        public long getItemId(int position) {
            return position;
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            ViewHolder vh=null;
            if(convertView==null){
                vh=new ViewHolder();
                convertView = mInflater.inflate(R.layout.listview_repair_record_item,null);
//                convertView.setBackgroundColor(Color.BLUE);
                TextView name = (TextView) convertView.findViewById(R.id.name);
                TextView daytime = (TextView) convertView.findViewById(R.id.daytime);
                vh.daytime=daytime;
                vh.name=name;
                convertView.setTag(vh);

            }else{
                vh= (ViewHolder) convertView.getTag();
            }
            try {
                final JSONObject jsonObject = repairRecordList.getJSONObject(position);
                vh.name.setText(jsonObject.getString("title"));
                vh.daytime.setText(jsonObject.getString("create_time"));
//                Log.e("task:","=======:"+jsonObject.toString());
                if(jsonObject.getBoolean("is_audit")){
                    convertView.setBackgroundColor(Color.parseColor("#66660000"));
                }else{
                    convertView.setBackgroundColor(Color.parseColor("#88006655"));

                }


            } catch (Exception e) {
                e.printStackTrace();
            }
            final JSONObject jsonObject;
            try {
                jsonObject = repairRecordList.getJSONObject(position);
                JSONObject task=null;
                convertView.setOnClickListener(new View.OnClickListener() {

                    @Override
                    public void onClick(View v) {

                        Intent intent=new Intent(RepairRecordActivity.this, RepairRecordItemActivity.class);
                        Bundle bundle=new Bundle();


                            bundle.putString("task",jsonObject.toString());
//                        Log.e("task:","=======:"+jsonObject.toString());
//                            bundle.putString("create_time",jsonObject.getString("create_time"));
                            intent.putExtras(bundle);

                        startActivity(intent);
                    }
                });
            } catch (JSONException e) {
                e.printStackTrace();
            }

            return convertView;
        }
    }
    class ViewHolder{
        public TextView name;
        public TextView daytime;
    }
    /*public void onListItemClick(ListView l,View v,int position,long id){
        Intent intent=new Intent(this, RepairActivity.class);
        startActivity(intent);
        super.onListItemClick(l, v, position, id);
    }*/
    private Map<String,Date> inputDate(final View v) {
        final Map<String,Date> map=new HashMap<String, Date>();

        Calendar cal = Calendar.getInstance();
        dialogCaldroidFragment=CaldroidFragment.newInstance("选择日期", cal.get(Calendar.MONTH)+1, cal.get(Calendar.YEAR));
        final String[] date_str = new String[1];
        dialogCaldroidFragment.setCaldroidListener(new CaldroidListener() {
            @Override
            public void onSelectDate(Date date, View view) {
                dialogCaldroidFragment.setBackgroundResourceForDate(R.color.light_blue,date);
                dialogCaldroidFragment.refreshView();

                date_str[0] = String.format("%tF", date);
                if(v instanceof EditText){
                    EditText e=(EditText)v;
                    e.setText(date_str[0]);

                }
                map.put(date_str[0],date);
                dialogCaldroidFragment.dismiss();
            }
        });

        dialogCaldroidFragment.show(getSupportFragmentManager(),"TAG");
        return  map;
    }
}
